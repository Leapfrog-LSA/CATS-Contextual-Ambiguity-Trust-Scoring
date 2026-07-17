from datetime import datetime, timezone
from typing import List

import structlog

from cats.signals.types import Message

logger = structlog.get_logger()


def normalize_messages(raw: List[dict]) -> List[Message]:
    """Phase 1: validate -> sort UTC -> dedup."""
    # (datetime, Message) pairs: sort on the real instant, not the ISO string —
    # mixed offsets (e.g. 10:00+02:00 vs 09:30Z) sort wrong lexicographically.
    dated: List[tuple] = []
    skipped = 0
    for m in raw:
        ts, text = m.get("timestamp"), m.get("text")
        # Reject anything that is not a non-empty string in either field
        # (str-only .strip()/fromisoformat) instead of crashing on e.g. an int.
        if not isinstance(ts, str) or not ts or not isinstance(text, str) or not text.strip():
            skipped += 1
            continue
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            # Treat a naive timestamp as UTC so naive and offset-aware inputs
            # can be sorted/deduped together (comparing them raises otherwise).
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            dated.append((dt, Message(timestamp=dt.isoformat(), text=text.strip(), metadata=m.get("metadata"))))
        except (ValueError, KeyError, TypeError):
            skipped += 1
            continue
    dated.sort(key=lambda pair: pair[0])
    seen: set = set()
    out: List[Message] = []
    for dt, msg in dated:
        # Dedup on the real instant + text: the UTC-normalised datetime, so the
        # same moment written with different offsets is one message, not two.
        k = (dt.astimezone(timezone.utc), msg.text)
        if k not in seen:
            seen.add(k)
            out.append(msg)
    dupes = len(dated) - len(out)
    if skipped or dupes:
        logger.info("normalize_messages", skipped=skipped, duplicates=dupes, accepted=len(out))
    return out
