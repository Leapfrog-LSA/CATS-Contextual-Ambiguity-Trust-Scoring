# CATS demo (Gradio)

A minimal public demo: paste a source URL, get its CATS trust score, band,
primary driver, per-signal breakdown, and any language/evidence/domain
warnings — with the ordinal-score disclaimer always visible. No signal logic
lives here; it's a thin UI over `cats.lite.score_feed`. No user data is
collected — each request is scored in memory and discarded; the only
server-side state is an in-memory per-session request counter for rate
limiting (~10 requests/minute/session).

## Run locally

```bash
pip install -r examples/demo/requirements.txt
python examples/demo/app.py
```

Opens on `http://127.0.0.1:7860`.

## Deploy as a Hugging Face Space

1. Create a new Space → SDK: **Gradio**.
2. Copy `app.py` and `requirements.txt` from this folder to the Space's root
   (the Space's `app.py` is its entry point — `demo.launch()` runs when the
   Space is built).
3. **Optional — full-fidelity NER coherence.** Without the spaCy Italian
   model, the demo still works: `coherence` degrades to a neutral,
   zero-confidence value (same graceful-degradation behaviour as everywhere
   else in CATS — it never crashes). For full fidelity, add this line to the
   Space's `requirements.txt` so the model wheel installs at build time:

   ```
   https://github.com/explosion/spacy-models/releases/download/it_core_news_lg-3.7.0/it_core_news_lg-3.7.0-py3-none-any.whl
   ```

   (Match the wheel version to the `spacy` version pinned in the main
   `pyproject.toml` if it has moved on since this was written.)
4. Push/commit — the Space builds and starts automatically.

## What's intentionally not here

- **No analytics or user-data collection** — the rate limiter only ever
  holds a request-count-per-session in memory, never the URLs scored.
- **No auth, no persistence** — this is the zero-infrastructure `cats.lite`
  path, same as the CLI; the audited, GDPR-compliant deployment is the
  separate FastAPI service (see the top-level [README](../../README.md)).
