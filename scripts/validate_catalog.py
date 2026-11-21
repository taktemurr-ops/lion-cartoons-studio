#!/usr/bin/env python3
"""Check production catalog and fail on unapproved releases."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
episodes = json.loads((ROOT / "content/episodes.json").read_text(encoding="utf-8"))
ids = set()
allowed = {"planned", "script_draft", "storyboard", "animating", "editing", "qa_pending", "approved", "published"}
for ep in episodes:
    assert ep["id"] not in ids, f"Duplicate episode: {ep['id']}"
    ids.add(ep["id"])
    assert ep["status"] in allowed, ep["id"]
    assert 0 <= ep["age_min"] <= ep["age_max"] <= 17, ep["id"]
    assert ep["language_source"] == "tr", ep["id"]
    if ep.get("script"):
        assert (ROOT / ep["script"]).exists(), ep["script"]
    if ep["status"] in {"approved", "published"}:
        assert ep["qa_approved"] is True, ep["id"]
        assert ep.get("master_video"), ep["id"]
print(f"OK: {len(episodes)} entries validated; no publishing authorized.")
