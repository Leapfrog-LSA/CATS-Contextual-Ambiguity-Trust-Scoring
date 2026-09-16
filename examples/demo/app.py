"""Gradio demo: score an OSINT source's trust straight from its URL.

Thin UI over cats.lite.score_feed — no signal logic lives here. Meant to be
deployed as a Hugging Face Space (see README.md in this folder); running it
locally with `python app.py` works the same way.

No user data is collected or persisted: each request is scored in memory and
discarded. The only server-side state is an in-memory per-session request
count used for basic rate limiting.
"""

from __future__ import annotations

import time
from collections import defaultdict
from typing import Dict, List, Tuple

import gradio as gr

from cats.lite import FeedFetchError, FeedNotFoundError, score_feed

_REPO_URL = "https://github.com/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring"

_DISCLAIMER = (
    "**Ordinal score, not a probability.** CATS ranks a source's behavioural reliability "
    "patterns over time — it does not fact-check content and is not a substitute for human "
    "judgement. See [architecture.md](" + _REPO_URL + "/blob/main/docs/architecture.md)."
)

# Simple in-memory rate limit: no external store, resets on restart, and is
# per Gradio session (not shared across users beyond counting requests).
_RATE_LIMIT = 10
_RATE_WINDOW_SECONDS = 60.0
_request_log: Dict[str, List[float]] = defaultdict(list)


def _rate_limited(session_key: str) -> bool:
    now = time.monotonic()
    recent = [t for t in _request_log[session_key] if now - t < _RATE_WINDOW_SECONDS]
    if len(recent) >= _RATE_LIMIT:
        _request_log[session_key] = recent
        return True
    recent.append(now)
    _request_log[session_key] = recent
    return False


def _signals_table(signals: Dict[str, float]) -> str:
    rows = "\n".join(f"| {name} | {value:.1f} |" for name, value in signals.items())
    return f"| Signal | Value |\n| --- | --- |\n{rows}"


def _format_result(result: dict) -> Tuple[str, str, str, str, str]:
    score_md = f"# {result['trust_score']:.1f}\n\n**Band:** `{result['band']}`"

    explanation = result.get("explanation") or {}
    driver = explanation.get("primary_driver")
    driver_md = f"**Primary driver:** {driver}" if driver else "_No explanation available._"

    signals_md = _signals_table(result["signals"])

    explanation_md = explanation.get("methodology", "")

    warnings = []
    if result["requires_human_review"]:
        warnings.append("⚠️ **Human review recommended** for this score.")
    language = result["language"]
    if language["detected"] == "other":
        warnings.append(
            "⚠️ Input does not look Italian: the default NLP stack is Italian-optimised, "
            "so signal quality is degraded for this source."
        )
    evidence = result["evidence"]
    if not evidence["sufficient"]:
        warnings.append(
            f"⚠️ Only {evidence['messages']} messages available (minimum "
            f"{evidence['min_messages']}) — evidence is thin."
        )
    if result["signals"].get("domain_provenance", 0) > 0:
        warnings.append("🚩 Domain-provenance red flags detected for this URL.")
    warnings_md = "\n\n".join(warnings) if warnings else "No warnings."

    return score_md, driver_md, signals_md, explanation_md, warnings_md


_EMPTY = ("", "", "", "", "")


def score_source(url: str, source_type: str, request: gr.Request) -> Tuple[str, str, str, str, str]:
    session_key = (getattr(request, "session_hash", None) or "anonymous") if request else "anonymous"
    if _rate_limited(session_key):
        return (*_EMPTY[:4], "⚠️ Rate limit reached (10 requests/minute) — please wait a moment.")

    if not url or not url.strip():
        return (*_EMPTY[:4], "Enter a source URL first.")

    try:
        result = score_feed(url.strip(), source_type=source_type, load_nlp=True)
    except (FeedNotFoundError, FeedFetchError) as exc:
        return (*_EMPTY[:4], f"❌ {exc}")
    except ValueError as exc:
        return (*_EMPTY[:4], f"❌ {exc}")

    return _format_result(result)


def build_demo() -> gr.Blocks:
    with gr.Blocks(title="CATS — Trust Intelligence for OSINT Sources") as demo:
        gr.Markdown("# CATS — Trust Intelligence for OSINT Sources")
        gr.Markdown(_DISCLAIMER)

        with gr.Row():
            url_input = gr.Textbox(label="Source URL", placeholder="https://example-news-outlet.it")
            source_type = gr.Dropdown(choices=["default", "news"], value="default", label="Source type")
        run_button = gr.Button("Score", variant="primary")

        score_output = gr.Markdown(label="Score")
        driver_output = gr.Markdown(label="Primary driver")
        signals_output = gr.Markdown(label="Signals")
        explanation_output = gr.Markdown(label="Methodology")
        warnings_output = gr.Markdown(label="Warnings")

        run_button.click(
            fn=score_source,
            inputs=[url_input, source_type],
            outputs=[score_output, driver_output, signals_output, explanation_output, warnings_output],
        )

        gr.Markdown(f"[CATS on GitHub]({_REPO_URL})")
        gr.Markdown(_DISCLAIMER)

    return demo


demo = build_demo()

if __name__ == "__main__":
    demo.launch()
