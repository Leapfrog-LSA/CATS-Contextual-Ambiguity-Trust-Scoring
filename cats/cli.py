"""Command-line interface: ``cats score <url>``.

A thin wrapper over :func:`cats.lite.score`/:func:`cats.lite.score_feed` — no
signal logic lives here; this module only parses arguments, calls the
library, and formats the result.
"""

from __future__ import annotations

import argparse
import contextlib
import json
import sys
from typing import List, Optional

from cats import __version__
from cats.lite import FeedFetchError, FeedNotFoundError, score, score_feed

_NOTE = "Ordinal score, not a probability. Cross-validate key claims. See docs/architecture.md."


def _load_messages(path: str) -> List[dict]:
    messages = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                messages.append(json.loads(line))
    return messages


def _load_weights(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _review_reason(result: dict) -> str:
    evidence = result["evidence"]
    if not evidence["sufficient"]:
        return f"insufficient evidence ({evidence['messages']} < {evidence['min_messages']} messages)"
    if result["band"] in ("low", "very_low"):
        return f"band {result['band']}"
    return "low-confidence signal(s)"


def _format_human(result: dict, url: Optional[str]) -> str:
    lines = []
    source = result.get("source")
    if source:
        first = source["first_timestamp"][:10]
        last = source["last_timestamp"][:10]
        lines.append(
            f"Source     {source['url']}   "
            f"(feed: {source['feed_url']}, {source['messages']} messages, {first} → {last})"
        )
    elif url:
        lines.append(f"Source     {url}")

    lines.append(f"Score      {result['trust_score']}   band: {result['band']}")

    explanation = result.get("explanation")
    if explanation and explanation.get("primary_driver"):
        driver = explanation["primary_driver"]
        share = next(
            (d["score_share_pct"] for d in explanation["signals"] if d["signal"] == driver),
            None,
        )
        if share is not None:
            lines.append(f"Driver     {driver} (share {share}%)")

    signals_line = " · ".join(f"{name} {value}" for name, value in result["signals"].items())
    lines.append(f"Signals    {signals_line}")

    language = result["language"]
    evidence = result["evidence"]
    evidence_mark = "✓" if evidence["sufficient"] else "✗"
    lines.append(
        f"Language   {language['detected']} ({language['confidence']})"
        f"      Evidence  {evidence['messages']} ≥ {evidence['min_messages']} {evidence_mark}"
    )

    if result["requires_human_review"]:
        lines.append(f"Review required: {_review_reason(result)}")
    if language["detected"] == "other":
        lines.append("Warning    Input does not look Italian: the default NLP stack is Italian-optimised (WP 4.1).")
    if result["signals"].get("domain_provenance", 0) > 0:
        reasons = []
        if explanation and explanation.get("domain_penalty"):
            reasons = explanation["domain_penalty"].get("metadata", {}).get("reasons", [])
        lines.append(f"Domain red flags: {', '.join(reasons) if reasons else 'present'}")

    lines.append(f"Note       {_NOTE}")
    return "\n".join(lines)


def _run_score(args: argparse.Namespace) -> int:
    weights = None
    if args.weights:
        try:
            weights = _load_weights(args.weights)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"error: could not read --weights file: {exc}", file=sys.stderr)
            return 2

    # Everything the library writes to stdout while scoring goes to stderr
    # instead, so stdout carries the result and nothing else. structlog is
    # unconfigured in the CLI and its default logger prints to *stdout*, so
    # without this the spaCy-load and feed-discovery lines land in front of the
    # report — and under --json they make the output unparseable
    # (`cats score <url> --json | jq` dies on the first log line). Redirecting
    # around the call, rather than reconfiguring structlog globally, keeps the
    # fix local: no global logging state is mutated (the API configures its own
    # JSON logging in `cats.api.main`), and stray prints from any dependency are
    # caught too.
    try:
        with contextlib.redirect_stdout(sys.stderr):
            if args.messages:
                try:
                    messages = _load_messages(args.messages)
                except (OSError, json.JSONDecodeError) as exc:
                    print(f"error: could not read --messages file: {exc}", file=sys.stderr)
                    return 2
                result = score(
                    messages,
                    source_type=args.source_type,
                    weights=weights,
                    load_nlp=not args.no_nlp,
                    url=args.url,
                )
            else:
                result = score_feed(
                    args.url,
                    source_type=args.source_type,
                    max_messages=args.max_messages,
                    weights=weights,
                    load_nlp=not args.no_nlp,
                )
    except (FeedNotFoundError, FeedFetchError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 4

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(_format_human(result, args.url))
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cats", description="CATS trust-intelligence scoring CLI.")
    parser.add_argument("--version", action="version", version=f"cats-scoring {__version__}")

    subparsers = parser.add_subparsers(dest="command")
    score_parser = subparsers.add_parser("score", help="Score a source from a URL/feed, or a messages file.")
    score_parser.add_argument("url", nargs="?", help="Source URL or feed URL (autodiscovers the feed).")
    score_parser.add_argument("--messages", help="Path to a JSONL file of {timestamp, text} messages.")
    score_parser.add_argument("--source-type", default="default", choices=["news", "default"])
    score_parser.add_argument("--json", action="store_true", help="Print the raw score() result as JSON.")
    score_parser.add_argument("--max-messages", type=int, default=200, help="Feed mode only: keep the latest N.")
    score_parser.add_argument("--weights", help="Path to a JSON file of signal-name -> weight overrides.")
    score_parser.add_argument("--no-nlp", action="store_true", help="Skip loading the spaCy NER model.")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = _build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        # argparse's --version/--help/parse-error paths call sys.exit() directly;
        # convert to a return so main() stays a plain function for tests and the
        # console-script entry point alike.
        return int(exc.code or 0)

    if args.command is None:
        parser.print_help(sys.stderr)
        return 2
    if not args.url and not args.messages:
        print("error: provide a URL or --messages FILE", file=sys.stderr)
        return 2

    return _run_score(args)


if __name__ == "__main__":
    sys.exit(main())
