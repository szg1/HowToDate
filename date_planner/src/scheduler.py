from __future__ import annotations
from datetime import datetime, timedelta

WEEKDAYS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

def propose_slots(now: datetime | None = None, minutes: int = 75) -> list[str]:
    """Return 5 candidate slots in local time for the next 10 days."""
    now = now or datetime.now()
    candidates = []
    windows = [(17, 30), (18, 0), (19, 0), (16, 30), (15, 30)]
    d = now
    while len(candidates) < 5 and (d - now).days <= 10:
        for h, m in windows:
            start = d.replace(hour=h, minute=m, second=0, microsecond=0)
            if start <= now:
                continue
            end = start + timedelta(minutes=minutes)
            stamp = f"{WEEKDAYS[start.weekday()]} {start:%Y-%m-%d} {start:%H:%M}–{end:%H:%M}"
            candidates.append(stamp)
            if len(candidates) >= 5:
                break
        d += timedelta(days=1)
    return candidates
