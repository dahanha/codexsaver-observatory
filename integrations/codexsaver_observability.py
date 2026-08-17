from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


def events_path() -> Path:
    configured = os.environ.get("CODEXSAVER_EVENTS_FILE", "").strip()
    return Path(configured).expanduser() if configured else Path.home() / ".codexsaver" / "events.jsonl"


def append_event(payload: dict[str, Any]) -> None:
    """Append one redacted routing event without ever breaking task execution."""
    try:
        path = events_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "event_id": str(uuid4()),
            "timestamp": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
            **payload,
        }
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    except (OSError, TypeError, ValueError):
        return
