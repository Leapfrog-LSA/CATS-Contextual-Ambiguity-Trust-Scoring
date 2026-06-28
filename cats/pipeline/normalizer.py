from datetime import datetime
from typing import List

import structlog

from cats.signals.types import Message

logger = structlog.get_logger()


def normalize_messages(raw: List[dict]) -> List[Message]:
    """Phase 1: validate -> sort UTC -> dedup."""
    msgs: List[Message] = []
    skipped = 0
    for m in raw:
        if not m.get("timestamp") or not m.get("text"):
            skipped += 1
            continue
        try:
            dt = datetime.fromisoformat(m["timestamp"].replace("Z", "+00:00"))
            msgs.append(Message(timestamp=dt.isoformat(), text=m["text"].strip(), metadata=m.get("metadata")))
        except (ValueError, KeyError):
            skipped += 1
            continue
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
