#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Lightweight structure linter for marimo notebooks.

This tool complements `marimo check` by looking for structure smells that
often show up when an EDA notebook starts drifting into scattered UI work
or notebook-local pseudo-components.

Usage:
    python marimo_lint.py notebook.py
    python marimo_lint.py notebook.py --json
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
from dataclasses import asdict, dataclass, field
from difflib import SequenceMatcher
from pathlib import Path


TEMP_EXPORT_PATTERN = re.compile(
    r"^(?:base|chart|chart_data|data|display|filtered|final|mask|output|result|selected|styled|subset|temp|tmp)\d*$"
)
COMMENT_CELL_PATTERN = re.compile(r"^#\s*%%\s*(?:\[([^\]]+)\])?", re.MULTILINE)

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


@dataclass(slots=True)
class Suggestion:
    rule_id: str
    severity: str
    message: str
    why_it_matters: str
    location: dict[str, int | str]
    confidence: str


@dataclass(slots=True)
class NotebookAnalysis:
    cells: list[Cell]
    producers: dict[str, str]
    consumers: dict[str, set[str]]


def is_app_cell_decorator(node: ast.expr) -> bool:
    if isinstance(node, ast.Call):
        node = node.func

    return (
        isinstance(node, ast.Attribute)
        and node.attr == "cell"
        and isinstance(node.value, ast.Name)
        and node.value.id == "app"
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

    ui_exports = [name for name in exported_names if ui_assignment_map.get(name, False)]
    referenced_names = extract_referenced_names(module)
    non_empty_lines = sum(1 for line in code.splitlines() if line.strip())
    has_ui = bool(ui_widget_types)
    has_presentation = bool(presentation_tags)
    has_transform = bool(transform_tags)
    has_loading = bool(load_tags)

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


def parse_decorator_cells(source: str) -> list[Cell]:
    try:
        module = parse_python_module(source)
    except SyntaxError:
        return []

    lines = source.splitlines()
    cells: list[Cell] = []

    for index, node in enumerate(module.body):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not any(is_app_cell_decorator(decorator) for decorator in node.decorator_list):
            continue
        if not node.body:
            continue

        start_line = node.body[0].lineno
        end_line = node.body[-1].end_lineno or node.body[-1].lineno
        raw_code = "\n".join(lines[start_line - 1 : end_line])
        code = textwrap.dedent(raw_code).strip()
        if not code:
            continue

        exported_names: list[str] = []
        last_statement = node.body[-1]
        if isinstance(last_statement, ast.Return):
            exported_names = extract_names_from_return(last_statement.value)

        cells.append(
            build_cell(
                cell_id=cleaned_cell_id(node.name, index),
                code=code,
                start_line=start_line,
                end_line=end_line,
                source_kind="decorator",
                exported_names=exported_names,
            )
        )

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

    return NotebookAnalysis(cells=cells, producers=producers, consumers=consumers)


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


def suggest_ui_scatter(analysis: NotebookAnalysis) -> list[Suggestion]:
    suggestions: list[Suggestion] = []
    cells = analysis.cells
    used_cells: set[str] = set()

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
            if len(run) >= 2:
                used_cells.update(cell.id for cell in run)
                suggestions.append(
                    Suggestion(
                        rule_id="ui-scatter",
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

    cell_index = {cell.id: index for index, cell in enumerate(cells)}
    for cell in cells:
        if cell.id in used_cells or not cell.is_ui_focused or not cell.ui_exports:
            continue

        first_consumer_index: int | None = None
        for export_name in cell.ui_exports:
            for consumer_id in analysis.consumers.get(export_name, set()):
                consumer_index = cell_index[consumer_id]
                if first_consumer_index is None or consumer_index < first_consumer_index:
                    first_consumer_index = consumer_index

        if first_consumer_index is None:
            continue

        gap = first_consumer_index - cell_index[cell.id]
        if gap >= 3:
            consumer = cells[first_consumer_index]
            suggestions.append(
                Suggestion(
                    rule_id="ui-scatter",
                    severity="suggestion",
                    message=(
                        f"UI exported from {cell.id} is only used much later in {consumer.id}"
                    ),
                    why_it_matters=(
                        "Readers must jump across several cells to connect a control "
                        "with the analysis step it affects."
                    ),
                    location=location_for(cell),
                    confidence="medium" if gap == 3 else "high",
                )
            )

    return suggestions


def suggest_export_surface(analysis: NotebookAnalysis) -> list[Suggestion]:
    suggestions: list[Suggestion] = []

    for cell in analysis.cells:
        exported_names = [name for name in cell.exported_names if not name.startswith("_")]
        if not exported_names:
            continue

        non_import_exports = stable_exported_names(cell)
        suspicious_exports = [
            name for name in non_import_exports if TEMP_EXPORT_PATTERN.match(name)
        ]
        mixed = len(responsibilities(cell)) >= 2

        should_warn = (
            len(non_import_exports) >= 6
            or (len(non_import_exports) >= 4 and (mixed or suspicious_exports))
            or (len(non_import_exports) >= 3 and mixed and len(suspicious_exports) >= 2)
        )
        if not should_warn:
            continue

        preview = ", ".join(non_import_exports[:5])
        if len(non_import_exports) > 5:
            preview += ", ..."

        if len(non_import_exports) >= 6:
            confidence = "high"
        elif suspicious_exports and mixed:
            confidence = "high"
        else:
            confidence = "medium"

        suggestions.append(
            Suggestion(
                rule_id="export-surface",
                severity="suggestion",
                message=(
                    f"{cell.id} exports a wide surface ({len(non_import_exports)} names): {preview}"
                ),
                why_it_matters=(
                    "A large export surface usually means the cell is carrying too "
                    "many responsibilities or leaking intermediate values into the graph."
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


def generate_suggestions(source: str) -> list[Suggestion]:
    analysis = analyze_notebook(source)
    suggestions = [
        *suggest_ui_scatter(analysis),
        *suggest_export_surface(analysis),
        *suggest_oversized_cell(analysis),
        *suggest_repeated_patterns(analysis),
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


def format_json_output(filepath: str, suggestions: list[Suggestion]) -> str:
    return json.dumps(
        {
            "file": filepath,
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
    args = parser.parse_args()

    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        raise SystemExit(1)

    source = filepath.read_text(encoding="utf-8")
    suggestions = generate_suggestions(source)

    if args.json:
        print(format_json_output(str(filepath), suggestions))
    else:
        print(format_text_output(str(filepath), suggestions))


if __name__ == "__main__":
    main()
