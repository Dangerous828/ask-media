#!/usr/bin/env python3
"""Check that genre cards declare a form range instead of one frozen form.

A card's `form` field says which production forms this genre supports. When every
card declares the same single value, the field stops being a range and becomes a
copy of one project's decision -- and the genre/age matrix collapses onto that
form: a wuxia card and a slice-of-life card then both claim to be the same kind
of show. That is exactly the overfitting this suite is supposed to prevent.

The check is structural, not editorial. It does not judge whether a given range
is *right*; it only refuses the degenerate cases that carry no information:

* a card with no `form` at all,
* a card whose `form` is a single value while other cards list several (one card
  claiming its genre fits exactly one form, while the same genre's neighbours
  admit three, is a copy-paste leftover rather than a claim),
* every card declaring the identical form set (no range anywhere).

Reads only. Never writes project files.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MINIMUM_PYTHON = (3, 9)
if sys.version_info < MINIMUM_PYTHON:
    raise SystemExit(
        "genre_card_check.py needs Python {}.{} or newer".format(*MINIMUM_PYTHON)
    )

FRONT_MATTER_END = "---"
FORM_KEY = "form:"


class CheckError(ValueError):
    """The cards cannot be checked at all."""


def _front_matter(text: str) -> dict[str, str]:
    """Read the leading `---` block as flat key/value pairs."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONT_MATTER_END:
        return {}
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == FRONT_MATTER_END:
            break
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip()
    return fields


def _forms(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def check(cards_dir: Path) -> dict:
    # A file where a directory is expected cannot hold cards; naming the type
    # error beats the old "no genre cards under <file>" message, which read
    # like an empty directory instead of a wrong argument.
    if cards_dir.is_file():
        raise CheckError(
            f"cards_dir must be a directory, got a file: {cards_dir}（应传入 references/genre-cards 目录）"
        )
    if not cards_dir.is_dir():
        raise CheckError(f"cards directory does not exist: {cards_dir}")
    cards = sorted(cards_dir.glob("*.md"))
    if not cards:
        raise CheckError(f"no genre cards under {cards_dir}")

    declared: dict[str, list[str]] = {}
    missing: list[str] = []
    for card in cards:
        fields = _front_matter(card.read_text(encoding="utf-8"))
        raw = fields.get(FORM_KEY.rstrip(":"))
        if not raw:
            missing.append(card.name)
            continue
        declared[card.name] = _forms(raw)

    findings: list[dict] = []
    for name in missing:
        findings.append({
            "code": "GENRE_FORM_MISSING",
            "card": name,
            "message": "card declares no form; the genre then has no stated "
                       "production-form range and downstream has to guess",
        })

    if not declared:
        raise CheckError(f"no card under {cards_dir} declares a form")

    # Every card identical is the failure this check exists for: the field says
    # nothing about the genre any more.
    distinct = {tuple(sorted(forms)) for forms in declared.values()}
    if len(distinct) == 1:
        only = next(iter(distinct))
        findings.append({
            "code": "GENRE_FORM_FROZEN",
            "card": "*",
            "message": f"all {len(declared)} cards declare the same form set "
                       f"{list(only)}; the field is then a copy of one project's "
                       f"decision rather than a per-genre range",
        })

    widest = max((len(forms) for forms in declared.values()), default=0)
    if widest > 1:
        for name, forms in declared.items():
            if len(forms) == 1:
                findings.append({
                    "code": "GENRE_FORM_NARROWER_THAN_NEIGHBOURS",
                    "card": name,
                    "message": f"card declares a single form {forms[0]} while other "
                               f"cards declare up to {widest}; confirm this genre "
                               f"really supports only one form, or widen the range",
                })

    return {
        "cards": len(cards),
        "declared": len(declared),
        "distinct_form_sets": len(distinct),
        "findings": findings,
        "status": "pass" if not findings else "fail",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "cards_dir",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "references" / "genre-cards",
        help="directory holding the genre cards (defaults to this skill's cards)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = check(args.cards_dir)
    except CheckError as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
