#!/usr/bin/env python3
from __future__ import annotations
import json, os, hashlib
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "data"

def half_hour_bucket(dt: datetime) -> int:
    """0 -> хвилини [00..29], 1 -> [30..59]"""
    return 0 if dt.minute < 30 else 1

def build_payload() -> dict:
    now = datetime.now(timezone.utc).replace(microsecond=0)
    raw = f"{now.isoformat()}|{os.urandom(8).hex()}"
    checksum = hashlib.sha256(raw.encode()).hexdigest()[:12]
    return {
        "ts_utc": now.isoformat(),
        "unix": int(now.timestamp()),
        "halfhour_bucket": half_hour_bucket(now),  # 0 або 1
        "checksum": checksum,
        "source": "half-hour-metronome/stdlib",
        "hint": "no external APIs; guaranteed diff per run"
    }

def main() -> int:
    payload = build_payload()
    day_dir = OUTDIR / datetime.now(timezone.utc).strftime("%Y-%m-%d")
    day_dir.mkdir(parents=True, exist_ok=True)
    fname = day_dir / f"{datetime.now(timezone.utc).strftime('%H%M%S')}.json"
    fname.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[update.py] wrote file: {fname.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
