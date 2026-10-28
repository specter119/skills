#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""
Build a sanitized skill-eval evidence report from agent conversation history.

The script uses xurl to search skill mentions, reads matched session files, then
separates consumer-like prompts from skill-maintenance prompts.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote


SKILL_PATTERNS = {
    "deep-research": [
        r"\bdeep-research\b",
        r"\bweb[- ]research\b",
        r"调研",
        r"研究",
        r"investigate",
        r"\bresearch\b",
        r"深入了解",
    ],
    "genimg": [
        r"\bgenimg\b",
        r"生成图片",
        r"画一张",
        r"配图",
        r"illustration",
        r"image generation",
    ],
    "marimo-style": [
        r"\bmarimo-style\b",
        r"\bmarimo-eda-prototype\b",
        r"\bmarimo\b",
        r"\beda\b",
        r"analysis notebook",
        r"exploratory notebook",
        r"prototype-first notebook",
    ],
    "msgraph-explore": [
        r"\bmsgraph-explore\b",
        r"\bmsgraph-fetch\b",
        r"microsoft graph",
        r"sharepoint",
        r"onedrive",
        r"onenote",
        r"fetch-onenote",
        r"fetch-onenote-page",
    ],
    "report-building": [
        r"\breport-building\b",
        r"报告",
        r"论文",
        r"thesis",
        r"formal document",
        r"\breport\b",
        r"文档",
    ],
    "slide-building": [
        r"\bslide-building\b",
        r"\bslides?\b",
        r"\bdeck\b",
        r"presentation",
        r"pitch deck",
        r"\bppt\b",
        r"幻灯片",
        r"演示",
    ],
    "thorough-digest": [
        r"\bthorough-digest\b",
        r"digest materials",
        r"batch analysis",
        r"summarize all",
        r"整理这些材料",
        r"批量分析",
        r"thorough review",
    ],
    "typst-authoring": [
        r"\btypst-authoring\b",
        r"\btypst\b",
        r"\.typ\b",
        r"touying",
        r"compile typst",
        r"typst deck",
    ],
}

MAINTENANCE_PATTERNS = [
    r"\bskill\b",
    r"\bskills\b",
    r"yao-meta-skill",
    r"SKILL\.md",
    r"\bevals?\b",
    r"trigger-cases",
    r"execution-cases",
    r"\breferences/\b",
    r"\breports/\b",
    r"agents/openai\.yaml",
    r"\brename\b",
    r"重命名",
    r"统一.*格式",
    r"优化.*skill",
    r"评估.*skill",
    r"refactor",
    r"subagent",
    r"subaget",
    r"folder 里所有的 skill",
    r"所有的 skill",
    r"load 一次 yao-meta-skill",
]

SANITIZE_PATTERNS = [
    (re.compile(r"agents://\S+"), "<AGENT_URI>"),
    (re.compile(r"https?://\S+"), "<URL>"),
    (re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b"), "<EMAIL>"),
    (
        re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.IGNORECASE,
        ),
        "<ID>",
    ),
    (re.compile(r"\b[0-9a-f]{7,40}\b", re.IGNORECASE), "<HASH>"),
    (re.compile(r"/home/[^\s)>'`]+"), "<PATH>"),
    (re.compile(r"@\S+\.(?:md|pdf|docx|pptx|csv|xlsx)\b"), "<ATTACHMENT>"),
    (re.compile(r"\b[a-zA-Z0-9.-]+\.(?:com|net|org|io|cn|local)\b"), "<HOST>"),
]


@dataclass(frozen=True)
class Evidence:
    skill: str
    source_kind: str
    classification: str
    text: str
    thread_source: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root used for repo-scoped xurl queries.",
    )
    parser.add_argument(
        "--providers",
        nargs="+",
        default=["codex", "pi"],
        help="Providers used when --global-history is enabled.",
    )
    parser.add_argument(
        "--limit-per-skill",
        type=int,
        default=20,
        help="Maximum matched threads fetched per skill query.",
    )
    parser.add_argument(
        "--max-evidence",
        type=int,
        default=5,
        help="Maximum examples shown per skill/category.",
    )
    parser.add_argument(
        "--global-history",
        action="store_true",
        help="Search all provider history instead of only the current repo scope.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/history-derived-evals.md"),
        help="Markdown report path.",
    )
    return parser.parse_args()


def run_xurl(uri: str) -> str:
    result = subprocess.run(
        ["xurl", uri],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def parse_thread_sources(xurl_output: str) -> list[Path]:
    sources: list[Path] = []
    seen: set[str] = set()
    for match in re.finditer(r"thread_source:\s+'([^']+)'", xurl_output):
        raw = match.group(1)
        if raw in seen:
            continue
        seen.add(raw)
        sources.append(Path(raw))
    return sources


def query_thread_sources(
    skill: str,
    repo_root: Path,
    providers: list[str],
    limit: int,
    global_history: bool,
) -> list[Path]:
    outputs: list[str] = []
    if global_history:
        for provider in providers:
            uri = f"{provider}?q={quote(skill)}&limit={limit}"
            try:
                outputs.append(run_xurl(uri))
            except subprocess.CalledProcessError as error:
                print(error.stderr.strip() or error.stdout.strip(), file=sys.stderr)
    else:
        uri = f"agents://{repo_root}?q={quote(skill)}&limit={limit}"
        outputs.append(run_xurl(uri))

    merged: list[Path] = []
    seen: set[Path] = set()
    for output in outputs:
        for source in parse_thread_sources(output):
            if source in seen:
                continue
            seen.add(source)
            merged.append(source)
    return merged


def iter_text_segments(content: list[dict[str, object]]) -> str:
    parts: list[str] = []
    for item in content:
        text = item.get("text")
        if isinstance(text, str):
            parts.append(text)
    return "\n".join(parts).strip()


def strip_boilerplate(text: str) -> str:
    cleaned = text
    if "# AGENTS.md instructions" in cleaned:
        if "</environment_context>" in cleaned:
            cleaned = cleaned.split("</environment_context>", 1)[1]
        elif "</INSTRUCTIONS>" in cleaned:
            cleaned = cleaned.split("</INSTRUCTIONS>", 1)[1]
    cleaned = re.sub(
        r"### Available skills.*?Safety and fallback:.*?$",
        "",
        cleaned,
        flags=re.S | re.M,
    )
    return cleaned.strip()


def sanitize_text(text: str) -> str:
    sanitized = strip_boilerplate(text)
    for pattern, replacement in SANITIZE_PATTERNS:
        sanitized = pattern.sub(replacement, sanitized)
    sanitized = re.sub(r"\b(19|20)\d{2}-\d{2}-\d{2}\b", "<DATE>", sanitized)
    sanitized = re.sub(r"\s+", " ", sanitized).strip()
    return sanitized


def should_ignore(text: str) -> bool:
    if not text or len(text) < 8:
        return True
    prefixes = ("<subagent_notification>", "Warning:", "The working copy")
    if text.startswith(prefixes):
        return True
    return False


def count_skill_mentions(text: str, known_skills: set[str]) -> int:
    lowered = text.lower()
    return sum(1 for skill in known_skills if skill in lowered)


def classify_text(text: str, source_kind: str, known_skills: set[str]) -> str:
    if source_kind == "delegated_task":
        return "maintenance"
    if count_skill_mentions(text, known_skills) >= 2:
        return "maintenance"
    for pattern in MAINTENANCE_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return "maintenance"
    return "consumer"


def matches_skill(skill: str, text: str) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in SKILL_PATTERNS[skill])


def load_thread_messages(thread_source: Path) -> list[tuple[str, str]]:
    messages: list[tuple[str, str]] = []
    if not thread_source.is_file():
        return messages

    try:
        lines = thread_source.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return messages

    for line in lines:
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue

        if item.get("type") != "response_item":
            continue

        payload = item.get("payload", {})
        payload_type = payload.get("type")

        if payload_type == "message" and payload.get("role") == "user":
            text = sanitize_text(iter_text_segments(payload.get("content", [])))
            if not should_ignore(text):
                messages.append(("user_prompt", text))
            continue

        if payload_type == "function_call" and payload.get("name") == "spawn_agent":
            arguments = payload.get("arguments")
            if not isinstance(arguments, str):
                continue
            try:
                parsed_arguments = json.loads(arguments)
            except json.JSONDecodeError:
                continue
            message = parsed_arguments.get("message")
            if not isinstance(message, str):
                continue
            text = sanitize_text(message)
            if not should_ignore(text):
                messages.append(("delegated_task", text))
    return messages


def collect_skill_evidence(
    skill: str,
    thread_sources: list[Path],
    known_skills: set[str],
) -> list[Evidence]:
    evidence: dict[tuple[str, str, str], Evidence] = {}
    cache: dict[Path, list[tuple[str, str]]] = {}

    for thread_source in thread_sources:
        if thread_source not in cache:
            cache[thread_source] = load_thread_messages(thread_source)
        for source_kind, text in cache[thread_source]:
            if not matches_skill(skill, text):
                continue
            classification = classify_text(text, source_kind, known_skills)
            key = (source_kind, classification, text)
            evidence.setdefault(
                key,
                Evidence(
                    skill=skill,
                    source_kind=source_kind,
                    classification=classification,
                    text=text,
                    thread_source=str(thread_source),
                ),
            )

    return list(evidence.values())


def render_report(
    repo_root: Path,
    evidence_by_skill: dict[str, list[Evidence]],
    thread_counts: dict[str, int],
    max_evidence: int,
    global_history: bool,
    providers: list[str],
) -> str:
    scope_label = "global provider history" if global_history else "repo-scoped history"
    lines = [
        "# History-Derived Eval Evidence",
        "",
        "This report is a review-first artifact derived from agent history.",
        "It helps decide which skills already have enough real usage to promote",
        "sanitized prompts into `evals/trigger-cases.md` and `evals/execution-cases.md`.",
        "",
        "## Scope",
        "",
        f"- Repo root: `{repo_root}`",
        f"- Search mode: `{scope_label}`",
        f"- Providers: `{', '.join(providers)}`",
        "",
        "## Summary",
        "",
        "| Skill | Matched Threads | Consumer Evidence | Maintenance Evidence | Recommendation |",
        "| --- | ---: | ---: | ---: | --- |",
    ]

    for skill, items in evidence_by_skill.items():
        consumer = sum(1 for item in items if item.classification == "consumer")
        maintenance = sum(1 for item in items if item.classification == "maintenance")
        if consumer >= 2:
            recommendation = "Good candidate for history-backed trigger seeds."
        elif consumer == 1:
            recommendation = "Only one direct sample; keep manual curation."
        elif maintenance > 0:
            recommendation = "Mostly skill-maintenance history; not enough runtime evidence."
        else:
            recommendation = "No trustworthy evidence found."
        lines.append(
            f"| `{skill}` | {thread_counts.get(skill, 0)} | {consumer} | {maintenance} | {recommendation} |"
        )

    lines.extend(["", "## Skill Details", ""])

    for skill, items in evidence_by_skill.items():
        consumer_items = [item for item in items if item.classification == "consumer"]
        maintenance_items = [item for item in items if item.classification == "maintenance"]
        lines.append(f"### `{skill}`")
        lines.append("")
        if not items:
            lines.append("- No evidence found.")
            lines.append("")
            continue

        if consumer_items:
            lines.append("#### Candidate Trigger / Execution Seeds")
            lines.append("")
            for item in consumer_items[:max_evidence]:
                lines.append(f"- {item.text}")
            lines.append("")

        if maintenance_items:
            lines.append("#### Maintenance-Only Evidence")
            lines.append("")
            for item in maintenance_items[:max_evidence]:
                lines.append(f"- {item.text}")
            lines.append("")

        lines.append("#### Notes")
        lines.append("")
        if consumer_items:
            lines.append(
                "- Consumer-like history exists. Promote only after checking that the prompt is not tied to one private repo, person, or incident."
            )
        else:
            lines.append(
                "- No trustworthy end-user prompt found. Keep current evals synthetic until more real usage is collected."
            )
        if maintenance_items:
            lines.append(
                "- Maintenance records are still useful, but they belong more to `yao-meta-skill` evaluation than to this skill's runtime routing boundary."
            )
        lines.append("")

    lines.extend(
        [
            "## Sanitization Rules Applied",
            "",
            "- Remove AGENTS boilerplate and environment preamble.",
            "- Replace local absolute paths, URLs, agent URIs, emails, UUID-like IDs, hashes, and attachment references.",
            "- Preserve public skill names and generic task wording so the prompt shape stays useful.",
            "",
            "## Limitations",
            "",
            "- This is still heuristic extraction; promotion into formal evals should stay manual.",
            "- Threads with explicit skill-name mentions are easier to recover than fully implicit invocations.",
            "- Repo-maintenance conversations can dominate the corpus when the skills repo itself is under active refactor.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    known_skills = set(sorted(SKILL_PATTERNS))
    evidence_by_skill: dict[str, list[Evidence]] = {}
    thread_counts: dict[str, int] = {}

    try:
        for skill in sorted(known_skills):
            thread_sources = query_thread_sources(
                skill=skill,
                repo_root=repo_root,
                providers=args.providers,
                limit=args.limit_per_skill,
                global_history=args.global_history,
            )
            thread_counts[skill] = len(thread_sources)
            evidence_by_skill[skill] = collect_skill_evidence(
                skill=skill,
                thread_sources=thread_sources,
                known_skills=known_skills,
            )
    except FileNotFoundError:
        print("xurl is not installed or not on PATH.", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as error:
        print(error.stderr.strip() or error.stdout.strip(), file=sys.stderr)
        return error.returncode

    report = render_report(
        repo_root=repo_root,
        evidence_by_skill=evidence_by_skill,
        thread_counts=thread_counts,
        max_evidence=args.max_evidence,
        global_history=args.global_history,
        providers=args.providers,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
