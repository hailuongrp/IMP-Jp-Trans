#!/usr/bin/env python3
"""Read-only checks for UTF-8 report text. No LLM, network, or quality score."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
import unicodedata

URL = re.compile(r"https?://[^\s<>\"'`]+")
CITATION = re.compile(r"\[(?:\^[\w-]+|(?:S|E|CF|DS|LC)[-_]?\d+|\d+)\]")
NUMBER = re.compile(r"(?<![A-Za-z0-9_])[-+−]?\d+(?:[.,]\d+)*(?:[%％])?")
ATTRIBUTION = re.compile(
    r"natural[-_ ]japanese|\bcoji\b|techtalk\.jp|powered\s+by|"
    r"translated\s+by|翻訳支援ツール|使用スキル", re.IGNORECASE
)


def urls(text: str) -> Counter[str]:
    # Heuristic for prose/Markdown. URLs with literal terminal punctuation need review.
    return Counter(match.rstrip(").,;:!?。）、") for match in URL.findall(text))


def numbers(text: str) -> Counter[str]:
    text = unicodedata.normalize("NFKC", text)
    text = URL.sub("", text)
    # Commas, dots, units and signs are deliberately not converted: ambiguous
    # locale/unit changes must be reconciled, not silently accepted as equivalent.
    return Counter(NUMBER.findall(text))


def diff(before: Counter[str], after: Counter[str]) -> dict[str, dict[str, int]]:
    return {"missing": dict(before - after), "added": dict(after - before)}


def check(source: str, target: str) -> dict:
    issues = []
    if not source.strip() or not target.strip():
        issues.append({"kind": "empty_input", "severity": "blocker"})
    checks = (
        ("urls", urls(source), urls(target)),
        ("citation_markers", Counter(CITATION.findall(source)), Counter(CITATION.findall(target))),
        ("numeric_tokens", numbers(source), numbers(target)),
    )
    for name, before, after in checks:
        delta = diff(before, after)
        if delta["missing"] or delta["added"]:
            issues.append({"kind": name, "severity": "review", **delta})
    source_credit = Counter(x.casefold() for x in ATTRIBUTION.findall(source))
    target_credit = Counter(x.casefold() for x in ATTRIBUTION.findall(target))
    added_credit = dict(target_credit - source_credit)
    if added_credit:
        issues.append({"kind": "new_tool_attribution", "severity": "review", "added": added_credit})
    return {
        "status": "REVIEW_REQUIRED" if issues else "NO_MECHANICAL_FLAGS",
        "semantic_review_required": True,
        "issues": issues,
        "limitations": "Heuristic text checks only; not translation approval. Does not verify meaning, source support, all citation formats, or hidden metadata. Review source-to-final directly.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    args = parser.parse_args(argv)
    try:
        result = check(args.source.read_text(encoding="utf-8"), args.target.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["issues"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
