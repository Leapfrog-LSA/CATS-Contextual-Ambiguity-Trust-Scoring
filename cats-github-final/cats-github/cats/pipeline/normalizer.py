from datetime import datetime
from typing import List
from cats.signals.types import Message


def normalize_messages(raw: List[dict]) -> List[Message]:
    """Phase 1: validate -> sort UTC -> dedup."""
    msgs: List[Message] = []
    for m in raw:
        if not m.get("timestamp") or not m.get("text"):
            continue
        try:
            dt = datetime.fromisoformat(m["timestamp"].replace("Z", "+00:00"))
            msgs.append(Message(timestamp=dt.isoformat(), text=m["text"].strip(),
                                metadata=m.get("metadata")))
        except (ValueError, KeyError):
            continue
    msgs.sort(key=lambda x: x.timestamp)
    seen, out = set(), []
    for m in msgs:
        k = (m.timestamp, m.text)
        if k not in seen:
            seen.add(k)
            out.append(m)
    return out
