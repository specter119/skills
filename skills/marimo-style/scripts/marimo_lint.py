#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///

"""
Lightweight structure linter for marimo notebooks.

This tool complements `marimo check` by looking for structure smells that
often show up when an EDA notebook starts drifting into scattered UI work
or notebook-local pseudo-components. It is a heuristic "worth a second look"
checker, not a correctness gate.

Usage:
    python marimo_lint.py notebook.py
    python marimo_lint.py notebook.py --style report
    python marimo_lint.py notebook.py --select export-surface,oversized-cell
    python marimo_lint.py notebook.py --style eda --ignore ui-far-consumer
    python marimo_lint.py notebook.py --json

Rules:
    shared (always run): ui-split-cells, export-surface, oversized-cell,
        repeated-pattern, control-upstream-impact
    --style eda adds:    ui-far-consumer
    --style report adds: control-zone-gap

    With no --style, only the shared rules run; the linter never infers style.
    --select replaces the preset with exactly the listed rules; --ignore
    removes rules from whatever set is active.

Per-cell suppression:
    A comment line `# marimo-lint: ignore[rule-id, ...]` inside a cell body
    suppresses those rules for suggestions located at that cell.
"""

from __future__ import annotations

import argparse
import ast
import io
import json
import keyword
import re
import sys
import textwrap
import tokenize
import warnings
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from difflib import SequenceMatcher
from pathlib import Path


TEMP_EXPORT_PATTERN = re.compile(
    r"^(?:base|chart|chart_data|data|display|filtered|final|mask|output|result|selected|styled|subset|temp|tmp)\d*$"
)
COMMENT_CELL_PATTERN = re.compile(r"^#\s*%%\s*(?:\[([^\]]+)\])?", re.MULTILINE)
SUPPRESSION_PATTERN = re.compile(r"#\s*marimo-lint:\s*ignore\[([^\]]+)\]")

APP_DECORATORS = {"cell", "function", "class_definition"}

# Selection widgets only behave as controls when another cell reads their
# selection back through `.value`; plain input widgets always count.
SELECTION_WIDGETS = {"altair_chart", "data_explorer", "dataframe", "plotly", "table"}

TRANSFORM_METHODS = {
    "agg",
    "apply",
    "assign",
    "drop",
    "filter",
    "groupby",
    "join",
    "melt",
    "merge",
    "pivot",
    "pivot_table",
    "query",
    "rename",
    "select",
    "sort",
    "sort_values",
    "transform",
    "with_columns",
}
LOAD_FUNCTIONS = {
    "connect",
    "open",
    "read_csv",
    "read_excel",
    "read_json",
    "read_parquet",
    "read_sql",
    "read_table",
    "scan_csv",
    "scan_parquet",
}
PRESENTATION_METHODS = {
    "Chart",
    "altair_chart",
    "bar",
    "hist",
    "html",
    "line",
    "markdown",
    "md",
    "plot",
    "scatter",
    "show",
    "table",
    "tabs",
    "vstack",
    "hstack",
}
TOKEN_KEEP_NAMES = (
    TRANSFORM_METHODS
    | LOAD_FUNCTIONS
    | PRESENTATION_METHODS
    | {
        "Path",
        "alt",
        "df",
        "go",
        "mo",
        "np",
        "pd",
        "pl",
        "plt",
        "px",
        "requests",
        "sns",
    }
)


@dataclass(slots=True)
class Cell:
    id: str
    code: str
    start_line: int
    end_line: int
    source_kind: str
    exported_names: list[str] = field(default_factory=list)
    imported_exports: list[str] = field(default_factory=list)
    ui_exports: list[str] = field(default_factory=list)
    referenced_names: set[str] = field(default_factory=set)
    ui_widget_types: set[str] = field(default_factory=set)
    presentation_tags: set[str] = field(default_factory=set)
    transform_tags: set[str] = field(default_factory=set)
    load_tags: set[str] = field(default_factory=set)
    non_empty_lines: int = 0
    top_level_assignments: int = 0
    normalized_signature: str = ""
    has_ui: bool = False
    has_presentation: bool = False
    has_transform: bool = False
    has_loading: bool = False
    is_ui_focused: bool = False
    has_visible_output: bool = False
    last_expression: str = ""
    last_expression_call: tuple[str, ...] = ()
    value_refs: set[str] = field(default_factory=set)
    display_refs: set[str] = field(default_factory=set)
    control_defs: dict[str, frozenset[str]] = field(default_factory=dict)
    suppressed_rules: set[str] = field(default_factory=set)


@dataclass(slots=True)
class Suggestion:
    rule_id: str
    severity: str
    message: str
    why_it_matters: str
    location: dict[str, int | str]
    confidence: str


@dataclass(slots=True)
class ControlInfo:
    name: str
    defining_cell: str
    display_cell: str
    widget_kinds: frozenset[str]
    affected_cells: set[str] = field(default_factory=set)


@dataclass(slots=True)
class NotebookAnalysis:
    cells: list[Cell]
    producers: dict[str, str]
    consumers: dict[str, set[str]]
    controls: dict[str, ControlInfo] = field(default_factory=dict)
    has_layout_file: bool = False


def app_decorator_kind(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str | None:
    for decorator in node.decorator_list:
        target = decorator.func if isinstance(decorator, ast.Call) else decorator
        if (
            isinstance(target, ast.Attribute)
            and isinstance(target.value, ast.Name)
            and target.value.id == "app"
            and target.attr in APP_DECORATORS
        ):
            return target.attr
    return None


def is_setup_block(node: ast.With) -> bool:
    return any(
        isinstance(item.context_expr, ast.Attribute)
        and item.context_expr.attr == "setup"
        and isinstance(item.context_expr.value, ast.Name)
        and item.context_expr.value.id == "app"
        for item in node.items
    )


def cleaned_cell_id(raw_name: str, index: int) -> str:
    stripped = raw_name.strip("_")
    return stripped or f"cell_{index}"


def extract_target_names(target: ast.expr) -> set[str]:
    names: set[str] = set()
    if isinstance(target, ast.Name):
        if not target.id.startswith("_"):
            names.add(target.id)
    elif isinstance(target, (ast.Tuple, ast.List)):
        for element in target.elts:
            names.update(extract_target_names(element))
    return names


def extract_names_from_return(expr: ast.expr | None) -> list[str]:
    if expr is None:
        return []
    if isinstance(expr, ast.Name):
        return [expr.id] if not expr.id.startswith("_") else []
    if isinstance(expr, (ast.Tuple, ast.List)):
        names: list[str] = []
        for element in expr.elts:
            names.extend(extract_names_from_return(element))
        return names
    if isinstance(expr, ast.Starred):
        return extract_names_from_return(expr.value)
    return []


def attr_chain(node: ast.AST) -> tuple[str, ...]:
    parts: list[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
        return tuple(reversed(parts))
    return ()


def contains_ui_call(node: ast.AST | None) -> bool:
    if node is None:
        return False
    for subnode in ast.walk(node):
        if isinstance(subnode, ast.Call):
            chain = attr_chain(subnode.func)
            if len(chain) >= 3 and chain[0] == "mo" and chain[1] == "ui":
                return True
    return False


def extract_top_level_exports(module: ast.Module) -> tuple[list[str], list[str], dict[str, bool], int]:
    exported_names: list[str] = []
    imported_exports: list[str] = []
    ui_assignment_map: dict[str, bool] = {}
    top_level_assignments = 0

    for statement in module.body:
        if isinstance(statement, ast.Assign):
            top_level_assignments += 1
            is_ui_assignment = contains_ui_call(statement.value)
            for target in statement.targets:
                for name in extract_target_names(target):
                    exported_names.append(name)
                    ui_assignment_map[name] = is_ui_assignment
        elif isinstance(statement, ast.AnnAssign):
            top_level_assignments += 1
            is_ui_assignment = contains_ui_call(statement.value)
            for name in extract_target_names(statement.target):
                exported_names.append(name)
                ui_assignment_map[name] = is_ui_assignment
        elif isinstance(statement, ast.AugAssign):
            top_level_assignments += 1
            for name in extract_target_names(statement.target):
                if name not in exported_names:
                    exported_names.append(name)
        elif isinstance(statement, ast.Import):
            for alias in statement.names:
                export_name = alias.asname or alias.name.split(".")[0]
                if export_name.startswith("_"):
                    continue
                exported_names.append(export_name)
                imported_exports.append(export_name)
        elif isinstance(statement, ast.ImportFrom):
            for alias in statement.names:
                export_name = alias.asname or alias.name
                if export_name.startswith("_"):
                    continue
                exported_names.append(export_name)
                imported_exports.append(export_name)
        elif isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not statement.name.startswith("_"):
                exported_names.append(statement.name)

    ordered_exports = list(dict.fromkeys(exported_names))
    ordered_imports = [name for name in dict.fromkeys(imported_exports) if name in ordered_exports]
    return ordered_exports, ordered_imports, ui_assignment_map, top_level_assignments


def extract_referenced_names(module: ast.Module) -> set[str]:
    return {
        node.id
        for node in ast.walk(module)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }


def parse_python_module(code: str) -> ast.Module:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        return ast.parse(code)


def final_display_statement(module: ast.Module) -> ast.Expr | None:
    statements = module.body
    if statements and isinstance(statements[-1], ast.Return):
        # A decorator cell's trailing `return` only declares exports; the
        # displayed output is the statement before it.
        statements = statements[:-1]
    if not statements:
        return None
    last = statements[-1]
    if not isinstance(last, ast.Expr):
        return None
    value = last.value
    # A bare None or a dangling string literal displays nothing.
    if isinstance(value, ast.Constant) and (value.value is None or isinstance(value.value, (str, bytes))):
        return None
    return last


def value_base_names(node: ast.AST) -> set[str]:
    return {
        subnode.value.id
        for subnode in ast.walk(node)
        if isinstance(subnode, ast.Attribute)
        and subnode.attr == "value"
        and isinstance(subnode.value, ast.Name)
    }


def display_name_refs(expr: ast.expr) -> set[str]:
    # A name displays a control when it appears as a bare element of the final
    # visible expression; occurrences only as the base of a `.value` read do not.
    display: set[str] = set()

    def visit(node: ast.AST, parent: ast.AST | None) -> None:
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if not (
                isinstance(parent, ast.Attribute)
                and parent.attr == "value"
                and parent.value is node
            ):
                display.add(node.id)
        for child in ast.iter_child_nodes(node):
            visit(child, node)

    visit(expr, None)
    return display



def normalize_code_for_similarity(code: str) -> str:
    normalized: list[str] = []
    try:
        for token in tokenize.generate_tokens(io.StringIO(code).readline):
            token_type = token.type
            token_str = token.string

            if token_type in {
                tokenize.COMMENT,
                tokenize.DEDENT,
                tokenize.ENCODING,
                tokenize.ENDMARKER,
                tokenize.INDENT,
                tokenize.NEWLINE,
                tokenize.NL,
            }:
                continue

            if token_type == tokenize.NAME:
                if keyword.iskeyword(token_str) or token_str in TOKEN_KEEP_NAMES:
                    normalized.append(token_str)
                else:
                    normalized.append("NAME")
            elif token_type == tokenize.NUMBER:
                normalized.append("NUM")
            elif token_type == tokenize.STRING:
                normalized.append("STR")
            else:
                normalized.append(token_str)
    except tokenize.TokenError:
        return ""

    return " ".join(normalized)


def analyze_code_features(
    code: str,
    exported_names: list[str],
    imported_exports: list[str],
    source_kind: str,
) -> Cell:
    module = parse_python_module(code)
    (
        _auto_exports,
        auto_imported_exports,
        ui_assignment_map,
        top_level_assignments,
    ) = extract_top_level_exports(module)
    imported_exports = list(
        dict.fromkeys(
            [
                *imported_exports,
                *(name for name in auto_imported_exports if name in exported_names),
            ]
        )
    )

    ui_widget_types: set[str] = set()
    presentation_tags: set[str] = set()
    transform_tags: set[str] = set()
    load_tags: set[str] = set()

    for node in ast.walk(module):
        if not isinstance(node, ast.Call):
            continue

        chain = attr_chain(node.func)
        if len(chain) >= 3 and chain[0] == "mo" and chain[1] == "ui":
            ui_widget_types.add(chain[2])
            continue

        method = chain[-1] if chain else ""

        if method in TRANSFORM_METHODS:
            transform_tags.add(method)
        if method in LOAD_FUNCTIONS:
            load_tags.add(method)

        if chain[:2] == ("mo", "output"):
            presentation_tags.add("output")
        elif chain[:2] == ("mo", "md"):
            presentation_tags.add("markdown")
        elif chain[:2] == ("mo", "html"):
            presentation_tags.add("html")
        elif len(chain) >= 2 and chain[0] == "alt" and chain[1] == "Chart":
            presentation_tags.add("altair")
        elif len(chain) >= 2 and chain[0] == "px":
            presentation_tags.add("plotly-express")
        elif len(chain) >= 2 and chain[0] == "plt":
            presentation_tags.add("matplotlib")
        elif len(chain) >= 2 and chain[0] == "sns":
            presentation_tags.add("seaborn")
        elif method in {"plot", "show"}:
            presentation_tags.add(method)
        elif method in {"vstack", "hstack", "tabs", "table"} and chain and chain[0] == "mo":
            presentation_tags.add(method)

    control_defs: dict[str, frozenset[str]] = {}
    for statement in module.body:
        if isinstance(statement, ast.Assign):
            rhs, targets = statement.value, statement.targets
        elif isinstance(statement, ast.AnnAssign):
            rhs, targets = statement.value, [statement.target]
        else:
            continue
        if rhs is None:
            continue
        # Any mo.ui.* constructor bound to a name makes it a control, even when
        # wrapped in mo.ui.array / .form() / .batch(); mo.ui.tabs is layout.
        kinds = {
            chain[2]
            for subnode in ast.walk(rhs)
            if isinstance(subnode, ast.Call)
            for chain in (attr_chain(subnode.func),)
            if len(chain) >= 3 and chain[0] == "mo" and chain[1] == "ui"
        }
        kinds.discard("tabs")
        if not kinds:
            continue
        for target in targets:
            for name in extract_target_names(target):
                control_defs[name] = frozenset(kinds)

    ui_exports = [name for name in exported_names if ui_assignment_map.get(name, False)]
    referenced_names = extract_referenced_names(module)
    non_empty_lines = sum(1 for line in code.splitlines() if line.strip())
    has_ui = bool(ui_widget_types)
    has_presentation = bool(presentation_tags)
    has_transform = bool(transform_tags)
    has_loading = bool(load_tags)

    final_expr = final_display_statement(module)
    has_visible_output = final_expr is not None
    last_expression = ast.unparse(final_expr.value) if final_expr else ""
    last_expression_call = (
        attr_chain(final_expr.value.func)
        if final_expr and isinstance(final_expr.value, ast.Call)
        else ()
    )
    value_refs = value_base_names(module)
    display_refs = display_name_refs(final_expr.value) if final_expr else set()

    suppressed_rules: set[str] = set()
    for match in SUPPRESSION_PATTERN.finditer(code):
        suppressed_rules.update(
            part.strip() for part in match.group(1).split(",") if part.strip()
        )

    cell = Cell(
        id="",
        code=code,
        start_line=0,
        end_line=0,
        source_kind=source_kind,
        exported_names=exported_names,
        imported_exports=imported_exports,
        ui_exports=ui_exports,
        referenced_names=referenced_names,
        ui_widget_types=ui_widget_types,
        presentation_tags=presentation_tags,
        transform_tags=transform_tags,
        load_tags=load_tags,
        non_empty_lines=non_empty_lines,
        top_level_assignments=top_level_assignments,
        normalized_signature=normalize_code_for_similarity(code),
        has_ui=has_ui,
        has_presentation=has_presentation,
        has_transform=has_transform,
        has_loading=has_loading,
        is_ui_focused=False,
        has_visible_output=has_visible_output,
        last_expression=last_expression,
        last_expression_call=last_expression_call,
        value_refs=value_refs,
        display_refs=display_refs,
        control_defs=control_defs,
        suppressed_rules=suppressed_rules,
    )
    cell.is_ui_focused = is_ui_focused(cell)
    return cell


def build_cell(
    cell_id: str,
    code: str,
    start_line: int,
    end_line: int,
    source_kind: str,
    exported_names: list[str] | None = None,
) -> Cell:
    exported_names = exported_names or []
    imported_exports: list[str] = []

    try:
        module = parse_python_module(code)
        if source_kind != "decorator":
            exported_names, imported_exports, _, _ = extract_top_level_exports(module)
    except SyntaxError:
        return Cell(
            id=cell_id,
            code=code,
            start_line=start_line,
            end_line=end_line,
            source_kind=source_kind,
            exported_names=exported_names,
            non_empty_lines=sum(1 for line in code.splitlines() if line.strip()),
        )

    analyzed = analyze_code_features(code, exported_names, imported_exports, source_kind)
    analyzed.id = cell_id
    analyzed.start_line = start_line
    analyzed.end_line = end_line
    return analyzed


def find_suppressions(text: str) -> set[str]:
    suppressed: set[str] = set()
    for match in SUPPRESSION_PATTERN.finditer(text):
        suppressed.update(
            part.strip() for part in match.group(1).split(",") if part.strip()
        )
    return suppressed


def parse_decorator_cells(source: str) -> list[Cell]:
    try:
        module = parse_python_module(source)
    except SyntaxError:
        return []

    lines = source.splitlines()
    cells: list[Cell] = []
    setup_seen = 0

    for index, node in enumerate(module.body):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            kind = app_decorator_kind(node)
            if kind is None:
                continue
            if kind == "cell":
                if not node.body:
                    continue
                exported_names: list[str] = []
                code_statements = node.body
                last_statement = node.body[-1]
                if isinstance(last_statement, ast.Return):
                    exported_names = extract_names_from_return(last_statement.value)
                    code_statements = node.body[:-1]
                if not code_statements:
                    continue

                start_line = code_statements[0].lineno
                end_line = code_statements[-1].end_lineno or code_statements[-1].lineno
                raw_code = "\n".join(lines[start_line - 1 : end_line])
                code = textwrap.dedent(raw_code).strip()
                if not code:
                    continue

                cell = build_cell(
                    cell_id=cleaned_cell_id(node.name, index),
                    code=code,
                    start_line=start_line,
                    end_line=end_line,
                    source_kind="decorator",
                    exported_names=exported_names,
                )
                # Suppression comments may sit above the first statement, so
                # scan the whole function region, not just the statement span.
                region_end = node.end_lineno or end_line
                cell.suppressed_rules |= find_suppressions(
                    "\n".join(lines[node.lineno - 1 : region_end])
                )
                cells.append(cell)
            else:
                # @app.function / @app.class_definition: the def itself is the
                # export; free names in the body become edges into this helper.
                start_line = node.lineno
                end_line = node.end_lineno or node.lineno
                raw_code = "\n".join(lines[start_line - 1 : end_line])
                code = textwrap.dedent(raw_code).strip()
                if not code:
                    continue
                cells.append(
                    build_cell(
                        cell_id=cleaned_cell_id(node.name, index),
                        code=code,
                        start_line=start_line,
                        end_line=end_line,
                        source_kind="helper",
                    )
                )
        elif isinstance(node, ast.With) and is_setup_block(node):
            if not node.body:
                continue
            setup_seen += 1
            cell_id = "setup" if setup_seen == 1 else f"setup_{setup_seen}"
            start_line = node.body[0].lineno
            end_line = node.body[-1].end_lineno or node.body[-1].lineno
            raw_code = "\n".join(lines[start_line - 1 : end_line])
            code = textwrap.dedent(raw_code).strip()
            if not code:
                continue
            cell = build_cell(
                cell_id=cell_id,
                code=code,
                start_line=start_line,
                end_line=end_line,
                source_kind="setup",
            )
            region_end = node.end_lineno or end_line
            cell.suppressed_rules |= find_suppressions(
                "\n".join(lines[node.lineno - 1 : region_end])
            )
            cells.append(cell)

    return cells


def parse_comment_cells(source: str) -> list[Cell]:
    matches = list(COMMENT_CELL_PATTERN.finditer(source))
    if not matches:
        return []

    cells: list[Cell] = []
    for index, match in enumerate(matches):
        cell_label = match.group(1) or f"cell_{index}"
        start_offset = match.end()
        end_offset = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        code = source[start_offset:end_offset].strip()
        if not code:
            continue

        start_line = source[:start_offset].count("\n") + 1
        end_line = start_line + max(code.count("\n"), 0)
        cells.append(
            build_cell(
                cell_id=cell_label,
                code=code,
                start_line=start_line,
                end_line=end_line,
                source_kind="comment",
            )
        )

    return cells


def parse_notebook(source: str) -> list[Cell]:
    decorator_cells = parse_decorator_cells(source)
    if decorator_cells:
        return decorator_cells

    comment_cells = parse_comment_cells(source)
    if comment_cells:
        return comment_cells

    return [
        build_cell(
            cell_id="main",
            code=source.strip(),
            start_line=1,
            end_line=max(source.count("\n") + 1, 1),
            source_kind="plain",
        )
    ]


def is_ui_focused(cell: Cell) -> bool:
    return (
        cell.has_ui
        and bool(cell.ui_exports)
        and not cell.has_loading
        and not cell.has_transform
        and not cell.has_presentation
        and cell.non_empty_lines <= 12
    )


def detects_layout_file(source: str) -> bool:
    try:
        module = parse_python_module(source)
    except SyntaxError:
        return False
    for node in ast.walk(module):
        if isinstance(node, ast.Call):
            chain = attr_chain(node.func)
            if chain and chain[-1] == "App" and any(
                keyword.arg == "layout_file" for keyword in node.keywords
            ):
                return True
    return False


def transitive_dependents(analysis: NotebookAnalysis, root_cell_ids: set[str]) -> set[str]:
    cell_map = {cell.id: cell for cell in analysis.cells}
    seen = set(root_cell_ids)
    stack = list(root_cell_ids)
    while stack:
        cell_id = stack.pop()
        for export_name in cell_map[cell_id].exported_names:
            for consumer_id in analysis.consumers.get(export_name, ()):
                if consumer_id not in seen:
                    seen.add(consumer_id)
                    stack.append(consumer_id)
    return seen


def detect_controls(analysis: NotebookAnalysis) -> dict[str, ControlInfo]:
    cells = analysis.cells
    controls: dict[str, ControlInfo] = {}

    for cell in cells:
        for name, kinds in cell.control_defs.items():
            if name in controls:
                continue
            if kinds <= SELECTION_WIDGETS and not any(
                name in other.value_refs for other in cells if other.id != cell.id
            ):
                continue
            controls[name] = ControlInfo(
                name=name,
                defining_cell=cell.id,
                display_cell=cell.id,
                widget_kinds=kinds,
            )

    for name, info in controls.items():
        # Display position, not definition position, drives the style rules:
        # where a control appears on the page is what readers orient by. The
        # whole notebook is searched because marimo notebooks routinely show a
        # control in a layout cell above the cell that defines it (the "attic"
        # pattern), and the visual position is what these rules care about.
        for cell in cells:
            if cell.has_visible_output and name in cell.display_refs:
                info.display_cell = cell.id
                break
        # Impact = reading the control's `.value`; a bare reference that only
        # places the widget inside a layout or list is display, not use.
        impact_cells = {cell.id for cell in cells if name in cell.value_refs}
        info.affected_cells = transitive_dependents(analysis, impact_cells)

    return controls


def analyze_notebook(source: str) -> NotebookAnalysis:
    cells = parse_notebook(source)
    producers: dict[str, str] = {}

    for cell in cells:
        for export_name in cell.exported_names:
            producers.setdefault(export_name, cell.id)

    consumers: dict[str, set[str]] = {}
    for cell in cells:
        for referenced_name in cell.referenced_names:
            producer = producers.get(referenced_name)
            if producer and producer != cell.id:
                consumers.setdefault(referenced_name, set()).add(cell.id)

    analysis = NotebookAnalysis(cells=cells, producers=producers, consumers=consumers)
    analysis.has_layout_file = detects_layout_file(source)
    analysis.controls = detect_controls(analysis)
    return analysis


def location_for(cell: Cell) -> dict[str, int | str]:
    return {
        "cell_id": cell.id,
        "line": cell.start_line,
        "end_line": cell.end_line,
    }


def responsibilities(cell: Cell) -> list[str]:
    result: list[str] = []
    if cell.has_ui:
        result.append("ui")
    if cell.has_loading or cell.has_transform:
        result.append("data")
    if cell.has_presentation:
        result.append("presentation")
    return result


def stable_exported_names(cell: Cell) -> list[str]:
    imported = set(cell.imported_exports)
    return [
        name
        for name in cell.exported_names
        if not name.startswith("_") and name not in imported
    ]


def is_narrative_presentation_cell(cell: Cell) -> bool:
    return (
        cell.has_presentation
        and not cell.has_ui
        and not cell.has_loading
        and not cell.has_transform
    )


def is_narrative_only_cell(cell: Cell, analysis: NotebookAnalysis) -> bool:
    # Static mo.md(...) prose between a control and its affected cells is
    # narration and does not break the control's zone; prose that reads other
    # cells' data is real output and does.
    if not (cell.has_visible_output and cell.last_expression_call[:2] == ("mo", "md")):
        return False
    cell_map = {item.id: item for item in analysis.cells}
    for name in cell.referenced_names:
        producer_id = analysis.producers.get(name)
        if producer_id is None or producer_id == cell.id:
            continue
        if name in cell_map[producer_id].imported_exports:
            continue
        return False
    return True


def is_ui_demo_cell(cell: Cell) -> bool:
    return (
        cell.has_ui
        and cell.has_presentation
        and not cell.has_loading
        and not cell.has_transform
    )


def is_repeated_pattern_candidate(cell: Cell) -> bool:
    return (
        cell.non_empty_lines >= 5
        and bool(cell.normalized_signature)
        and not is_narrative_presentation_cell(cell)
        and (cell.has_ui or cell.has_transform)
    )


def is_dependent_control_chain(run: list[Cell]) -> bool:
    # marimo forces a control whose options derive from another control's
    # `.value` into its own cell, so back-to-back dependent controls are fine.
    return all(
        run[position].referenced_names & set(run[position - 1].ui_exports)
        for position in range(1, len(run))
    )


def suggest_ui_split_cells(analysis: NotebookAnalysis) -> list[Suggestion]:
    suggestions: list[Suggestion] = []
    cells = analysis.cells

    run_start: int | None = None
    for index, cell in enumerate(cells + [Cell("", "", 0, 0, "sentinel")]):
        is_run_cell = index < len(cells) and cells[index].is_ui_focused
        if is_run_cell and run_start is None:
            run_start = index
            continue
        if is_run_cell:
            continue
        if run_start is not None:
            run = cells[run_start:index]
            if len(run) >= 2 and not is_dependent_control_chain(run):
                suggestions.append(
                    Suggestion(
                        rule_id="ui-split-cells",
                        severity="suggestion",
                        message=(
                            "UI controls are split across consecutive cells: "
                            + ", ".join(cell.id for cell in run)
                        ),
                        why_it_matters=(
                            "One exploration step now spans multiple cells, which "
                            "makes the notebook harder to scan and reason about locally."
                        ),
                        location=location_for(run[0]),
                        confidence="high" if len(run) >= 3 else "medium",
                    )
                )
            run_start = None

    return suggestions


def suggest_export_surface(analysis: NotebookAnalysis) -> list[Suggestion]:
    suggestions: list[Suggestion] = []

    for cell in analysis.cells:
        non_import_exports = stable_exported_names(cell)
        if not non_import_exports:
            continue

        generic_exports = [
            name for name in non_import_exports if TEMP_EXPORT_PATTERN.match(name)
        ]
        scopes = responsibilities(cell)
        wide_and_mixed = len(non_import_exports) >= 4 and len(scopes) >= 2
        if not generic_exports and not wide_and_mixed:
            continue

        if generic_exports:
            preview = ", ".join(generic_exports[:5])
            if len(generic_exports) > 5:
                preview += ", ..."
            message = f"{cell.id} exports generic name(s) that hide intent: {preview}"
        else:
            message = (
                f"{cell.id} exports {len(non_import_exports)} names while mixing "
                f"{', '.join(scopes)}"
            )

        if (generic_exports and len(scopes) >= 2) or len(generic_exports) >= 2:
            confidence = "high"
        else:
            confidence = "medium"

        suggestions.append(
            Suggestion(
                rule_id="export-surface",
                severity="suggestion",
                message=message,
                why_it_matters=(
                    "Rename the export to a semantic name that says what the value "
                    "is, or split the cell so each export carries one "
                    "responsibility; generic or sprawling exports make downstream "
                    "dependencies hard to trace."
                ),
                location=location_for(cell),
                confidence=confidence,
            )
        )

    return suggestions


def suggest_oversized_cell(analysis: NotebookAnalysis) -> list[Suggestion]:
    suggestions: list[Suggestion] = []

    for cell in analysis.cells:
        scopes = responsibilities(cell)
        responsibility_count = len(scopes)
        exported_names = stable_exported_names(cell)
        narrative_presentation = (
            is_narrative_presentation_cell(cell) and len(exported_names) <= 1
        )
        ui_demo = is_ui_demo_cell(cell) and len(exported_names) <= 2

        long_threshold = 52 if narrative_presentation else 36 if ui_demo else 32
        mixed_threshold = 26 if ui_demo else 20

        too_long = cell.non_empty_lines >= long_threshold
        mixed_cell = (
            not narrative_presentation
            and cell.non_empty_lines >= mixed_threshold
            and responsibility_count >= 2
        )
        dense_prototype = (
            cell.non_empty_lines >= 16
            and responsibility_count >= 3
            and len(exported_names) >= 3
            and cell.top_level_assignments >= 4
        )

        if not (too_long or mixed_cell or dense_prototype):
            continue

        if narrative_presentation:
            confidence = "medium" if cell.non_empty_lines >= 64 else "low"
        elif too_long and (
            responsibility_count >= 2
            or len(exported_names) >= 6
            or cell.top_level_assignments >= 8
        ):
            confidence = "high"
        elif responsibility_count >= 3 or dense_prototype:
            confidence = "medium"
        else:
            confidence = "low"

        scope_label = ", ".join(scopes) if scopes else "multiple concerns"
        suggestions.append(
            Suggestion(
                rule_id="oversized-cell",
                severity="suggestion",
                message=(
                    f"{cell.id} is carrying a large cell body ({cell.non_empty_lines} non-empty lines) "
                    f"across {scope_label}"
                ),
                why_it_matters=(
                    "When UI, transformation, and presentation accumulate in one "
                    "cell, the notebook starts behaving like a notebook-local component."
                ),
                location=location_for(cell),
                confidence=confidence,
            )
        )

    return suggestions


def suggest_control_upstream_impact(analysis: NotebookAnalysis) -> list[Suggestion]:
    suggestions: list[Suggestion] = []
    cells = analysis.cells
    cell_index = {cell.id: index for index, cell in enumerate(cells)}

    for name, info in analysis.controls.items():
        display_index = cell_index[info.display_cell]
        upstream = [
            cell
            for cell in cells[:display_index]
            if cell.id in info.affected_cells and cell.has_visible_output
        ]
        if not upstream:
            continue
        display_cell = cells[display_index]
        suggestions.append(
            Suggestion(
                rule_id="control-upstream-impact",
                severity="suggestion",
                message=(
                    f"Control `{name}` drives {upstream[0].id}, which is shown "
                    "above the control"
                ),
                why_it_matters=(
                    "A control placed below the content it changes makes readers "
                    "see outputs before the decision that produces them; move the "
                    "control (or its display) above the affected content."
                ),
                location=location_for(display_cell),
                confidence="medium",
            )
        )

    return suggestions


def visible_rank(cells: list[Cell], index: int) -> int:
    # Position of a cell when only visible-output cells are counted; hidden
    # cells do not add reading distance on the rendered page.
    return sum(1 for cell in cells[:index] if cell.has_visible_output)


def suggest_ui_far_consumer(analysis: NotebookAnalysis) -> list[Suggestion]:
    suggestions: list[Suggestion] = []
    cells = analysis.cells
    cell_index = {cell.id: index for index, cell in enumerate(cells)}

    for name, info in analysis.controls.items():
        display_index = cell_index[info.display_cell]
        consumers = [
            cell
            for cell in cells
            if cell.id != info.defining_cell
            and name in cell.value_refs
            and cell_index[cell.id] > display_index
        ]
        if not consumers:
            continue

        first_consumer = min(consumers, key=lambda cell: cell_index[cell.id])
        gap = visible_rank(cells, cell_index[first_consumer.id]) - visible_rank(
            cells, display_index
        )
        if gap < 3:
            continue

        defining_cell = cells[cell_index[info.defining_cell]]
        suggestions.append(
            Suggestion(
                rule_id="ui-far-consumer",
                severity="suggestion",
                message=(
                    f"Control `{name}` is displayed in {info.display_cell} but "
                    f"first used {gap} visible cells later in {first_consumer.id}"
                ),
                why_it_matters=(
                    "Readers must jump across several cells to connect a control "
                    "with the analysis step it affects."
                ),
                location=location_for(defining_cell),
                confidence="medium" if gap == 3 else "high",
            )
        )

    return suggestions


def suggest_control_zone_gap(analysis: NotebookAnalysis) -> list[Suggestion]:
    if analysis.has_layout_file:
        return []

    suggestions: list[Suggestion] = []
    cells = analysis.cells
    cell_index = {cell.id: index for index, cell in enumerate(cells)}
    reported_cells: set[str] = set()

    for name, info in analysis.controls.items():
        display_index = cell_index[info.display_cell]
        affected_visible_after = [
            index
            for index, cell in enumerate(cells)
            if index > display_index
            and cell.id in info.affected_cells
            and cell.has_visible_output
        ]
        if not affected_visible_after:
            continue

        zone_end = max(affected_visible_after)
        for index in range(display_index + 1, zone_end):
            cell = cells[index]
            if not cell.has_visible_output or cell.id in info.affected_cells:
                continue
            if is_narrative_only_cell(cell, analysis):
                continue
            if cell.id in reported_cells:
                continue
            reported_cells.add(cell.id)
            suggestions.append(
                Suggestion(
                    rule_id="control-zone-gap",
                    severity="suggestion",
                    message=(
                        f"{cell.id} sits between control `{name}` (displayed in "
                        f"{info.display_cell}) and its last affected cell but "
                        "does not respond to it"
                    ),
                    why_it_matters=(
                        "Output inside a control's zone that ignores the control "
                        "reads as if it were controlled; move it out of the zone "
                        "or make the dependency explicit."
                    ),
                    location=location_for(cell),
                    confidence="medium",
                )
            )

    return suggestions


def shared_feature_count(left: Cell, right: Cell) -> int:
    shared = 0
    if left.ui_widget_types & right.ui_widget_types:
        shared += 1
    if left.presentation_tags & right.presentation_tags:
        shared += 1
    if left.transform_tags & right.transform_tags:
        shared += 1
    if left.has_ui and right.has_ui:
        shared += 1
    return shared


def repeated_pattern_groups(analysis: NotebookAnalysis) -> list[tuple[list[Cell], float]]:
    cells = analysis.cells
    edges: dict[str, set[str]] = {}
    max_similarity_by_cell: dict[str, float] = {}
    cell_map = {cell.id: cell for cell in cells}

    for left_index, left in enumerate(cells):
        if not is_repeated_pattern_candidate(left):
            continue
        for right in cells[left_index + 1 :]:
            if not is_repeated_pattern_candidate(right):
                continue

            similarity = SequenceMatcher(
                None, left.normalized_signature, right.normalized_signature
            ).ratio()
            shared_features = shared_feature_count(left, right)
            if similarity < 0.88 and not (similarity >= 0.82 and shared_features >= 2):
                continue

            edges.setdefault(left.id, set()).add(right.id)
            edges.setdefault(right.id, set()).add(left.id)
            max_similarity_by_cell[left.id] = max(
                similarity, max_similarity_by_cell.get(left.id, 0.0)
            )
            max_similarity_by_cell[right.id] = max(
                similarity, max_similarity_by_cell.get(right.id, 0.0)
            )

    groups: list[tuple[list[Cell], float]] = []
    visited: set[str] = set()
    for cell_id in edges:
        if cell_id in visited:
            continue
        stack = [cell_id]
        component: list[str] = []
        max_similarity = 0.0
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            component.append(current)
            max_similarity = max(max_similarity, max_similarity_by_cell.get(current, 0.0))
            stack.extend(edges.get(current, set()) - visited)

        if len(component) >= 2:
            group_cells = sorted((cell_map[cell] for cell in component), key=lambda item: item.start_line)
            groups.append((group_cells, max_similarity))

    return groups


def suggest_repeated_patterns(analysis: NotebookAnalysis) -> list[Suggestion]:
    suggestions: list[Suggestion] = []

    for group, max_similarity in repeated_pattern_groups(analysis):
        if len(group) > 6 and max_similarity < 0.92:
            continue

        preview_cells = group[:5]
        cell_ids = ", ".join(cell.id for cell in preview_cells)
        if len(group) > len(preview_cells):
            cell_ids += f", ... (+{len(group) - len(preview_cells)} more)"
        confidence = "high" if max_similarity >= 0.88 or len(group) >= 3 else "medium"
        suggestions.append(
            Suggestion(
                rule_id="repeated-pattern",
                severity="suggestion",
                message=f"Similar interaction or presentation patterns repeat across {cell_ids}",
                why_it_matters=(
                    "A repeated notebook-local pattern often means the prototype shape "
                    "is stabilizing and is ready for a helper or module."
                ),
                location=location_for(group[0]),
                confidence=confidence,
            )
        )

    return suggestions


@dataclass(frozen=True, slots=True)
class RuleSpec:
    scope: str  # "shared" | "eda" | "report"
    check: Callable[[NotebookAnalysis], list[Suggestion]]


RULE_REGISTRY: dict[str, RuleSpec] = {
    "ui-split-cells": RuleSpec("shared", suggest_ui_split_cells),
    "export-surface": RuleSpec("shared", suggest_export_surface),
    "oversized-cell": RuleSpec("shared", suggest_oversized_cell),
    "repeated-pattern": RuleSpec("shared", suggest_repeated_patterns),
    "control-upstream-impact": RuleSpec("shared", suggest_control_upstream_impact),
    "ui-far-consumer": RuleSpec("eda", suggest_ui_far_consumer),
    "control-zone-gap": RuleSpec("report", suggest_control_zone_gap),
}


def rules_for_style(style: str | None) -> list[str]:
    scopes = ("shared",) if style is None else ("shared", style)
    return sorted(
        rule_id for rule_id, spec in RULE_REGISTRY.items() if spec.scope in scopes
    )


def split_rule_list(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def resolve_active_rules(
    style: str | None = None,
    select: str | None = None,
    ignore: str | None = None,
) -> list[str]:
    if select:
        rules = split_rule_list(select)
        unknown = sorted(set(rules) - set(RULE_REGISTRY))
        if unknown:
            raise ValueError(f"unknown rule id(s): {', '.join(unknown)}")
    else:
        rules = rules_for_style(style)

    if ignore:
        ignored = split_rule_list(ignore)
        unknown = sorted(set(ignored) - set(RULE_REGISTRY))
        if unknown:
            raise ValueError(f"unknown rule id(s): {', '.join(unknown)}")
        rules = [rule_id for rule_id in rules if rule_id not in ignored]

    return sorted(dict.fromkeys(rules))


def generate_suggestions(
    source: str, active_rules: list[str] | None = None
) -> list[Suggestion]:
    analysis = analyze_notebook(source)
    rule_ids = active_rules if active_rules is not None else rules_for_style(None)
    suggestions: list[Suggestion] = []
    for rule_id in rule_ids:
        suggestions.extend(RULE_REGISTRY[rule_id].check(analysis))

    suppressed = {
        cell.id: cell.suppressed_rules
        for cell in analysis.cells
        if cell.suppressed_rules
    }
    if suppressed:
        suggestions = [
            suggestion
            for suggestion in suggestions
            if suggestion.rule_id
            not in suppressed.get(str(suggestion.location.get("cell_id")), set())
        ]

    suggestions.sort(key=lambda item: (item.location["line"], item.rule_id, item.message))
    return suggestions


def format_text_output(filepath: str, suggestions: list[Suggestion]) -> str:
    if not suggestions:
        return f"✅ {filepath}: No structure suggestions"

    lines = [f"💡 {filepath}: {len(suggestions)} suggestion(s)", ""]
    for suggestion in suggestions:
        location = suggestion.location
        lines.append(
            f"  [{suggestion.rule_id}] {location['cell_id']}:{location['line']} {suggestion.message}"
        )
        lines.append(
            f"     why: {suggestion.why_it_matters}"
        )
        lines.append(
            f"     confidence: {suggestion.confidence}"
        )
    return "\n".join(lines)


def format_json_output(
    filepath: str,
    suggestions: list[Suggestion],
    style: str | None,
    rules_run: list[str],
) -> str:
    return json.dumps(
        {
            "file": filepath,
            "style": style,
            "rules_run": rules_run,
            "suggestion_count": len(suggestions),
            "suggestions": [asdict(suggestion) for suggestion in suggestions],
        },
        indent=2,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lightweight structure linter for marimo notebooks"
    )
    parser.add_argument("file", help="Notebook file to inspect")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    parser.add_argument(
        "--style",
        choices=["eda", "report"],
        default=None,
        help="Notebook style preset; without it only shared rules run",
    )
    parser.add_argument(
        "--select",
        default=None,
        help="Comma-separated rule ids to run, replacing the preset",
    )
    parser.add_argument(
        "--ignore",
        default=None,
        help="Comma-separated rule ids to remove from the active set",
    )
    args = parser.parse_args()

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        raise SystemExit(1)

    try:
        rules_run = resolve_active_rules(style=args.style, select=args.select, ignore=args.ignore)
    except ValueError as error:
        print(
            f"Error: {error}. Valid rule ids: {', '.join(sorted(RULE_REGISTRY))}",
            file=sys.stderr,
        )
        raise SystemExit(2) from error

    source = filepath.read_text(encoding="utf-8")
    suggestions = generate_suggestions(source, rules_run)

    if args.json:
        print(format_json_output(str(filepath), suggestions, args.style, rules_run))
    else:
        print(format_text_output(str(filepath), suggestions))


if __name__ == "__main__":
    main()
