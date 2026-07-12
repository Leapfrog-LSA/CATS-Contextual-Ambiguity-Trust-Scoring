from datetime import datetime, timezone
from typing import List, Optional

import structlog

from cats.signals.types import Message

logger = structlog.get_logger()


def _parse_utc(ts: str) -> Optional[datetime]:
    """Parse an ISO-8601 timestamp to an aware UTC datetime (None if invalid).

    Naive timestamps are taken as UTC. Converting every offset to UTC keeps
    chronological order identical to lexicographic order on the stored ISO
    strings — mixed offsets sorted as raw strings would order wrongly and skew
    the temporal signals (silence, volatility).
    """
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def normalize_messages(raw: List[dict]) -> List[Message]:
    """Phase 1: validate -> normalise to UTC -> sort -> dedup.

    Malformed entries (non-dict records, non-string timestamp/text, unparseable
    timestamps) are counted and skipped — library callers pass arbitrary input
    and must get a scored result or a clear error, never an AttributeError.
    """
    msgs: List[Message] = []
    skipped = 0
    for m in raw:
        if not isinstance(m, dict):
            skipped += 1
            continue
        ts, text = m.get("timestamp"), m.get("text")
        if not isinstance(ts, str) or not isinstance(text, str) or not ts or not text:
            skipped += 1
            continue
        dt = _parse_utc(ts)
        if dt is None:
            skipped += 1
            continue
        msgs.append(Message(timestamp=dt.isoformat(), text=text.strip(), metadata=m.get("metadata")))
    msgs.sort(key=lambda x: x.timestamp)
    seen: set = set()
    out: List[Message] = []
    for msg in msgs:
        k = (msg.timestamp, msg.text)
        if k not in seen:
            seen.add(k)
            out.append(msg)
    dupes = len(msgs) - len(out)
    if skipped or dupes:
        logger.info("normalize_messages", skipped=skipped, duplicates=dupes, accepted=len(out))
    return out
