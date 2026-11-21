#!/usr/bin/env python3
"""Fail-closed episode preflight. Does NOT render or publish."""
import argparse
import json
from pathlib import Path

def check(root: Path, manifest: Path, release: bool):
    data = json.loads(manifest.read_text(encoding="utf-8"))
    errors = []
    shots = data.get("shots", [])
    if data.get("frame_rate") != 24 or data.get("resolution") != [1920,1080]:
        errors.append("Master spec must be 1080p/24fps")
    if not shots:
        errors.append("No shot list")
    elif shots[0]["start_seconds"] != 0 or shots[-1]["end_seconds"] != data["target_seconds"]:
        errors.append("Incomplete timeline")
    for prev, current in zip(shots, shots[1:]):
        if prev["end_seconds"] != current["start_seconds"]:
            errors.append(f"Timeline gap/overlap: {prev['id']} -> {current['id']}")
    required_assets = [c["asset"] for c in data["characters"]]
    required_assets += [data["environment"]["asset"]]
    required_assets += [s["deliverable"] for s in shots]
    required_assets += [data["audio"][x] for x in ("music_master","sfx_master","dialogue_master","mix_master","license_register")]
    required_assets += list(data["subtitles"].values())
    required_assets.append(data["master_output"])
    for path in required_assets:
        target = root / path
        if not target.is_file() or target.stat().st_size == 0:
            errors.append(f"Missing/nonempty production asset: {path}")
    if release:
        if data.get("status") != "approved" or data.get("publish_approved") is not True:
            errors.append("Episode lacks explicit human publication approval")
        gate = root / "production/quality/S01E01_signoff.json"
        if not gate.exists():
            errors.append("Missing signed-off QA checklist")
        else:
            qa = json.loads(gate.read_text(encoding="utf-8"))
            for key in data["checks"]:
                if qa.get(key) is not True:
                    errors.append("QA not approved: "+key)
    return errors

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--release", action="store_true")
    a=p.parse_args()
    root=Path(__file__).resolve().parents[2]
    manifest=root/"production/quality/episode01_manifest.json"
    data=json.loads(manifest.read_text(encoding="utf-8"))
    assert len(data["shots"]) == 8
    errors=check(root,manifest,a.release)
    print(f"EPISODE {data['episode']} | target={data['target_seconds']}s | scenes={len(data['shots'])} | status={data['status']}")
    for e in errors: print("BLOCKER:",e)
    print(f"Production assets missing: {len(errors)}. Release: {'BLOCKED' if errors else 'READY FOR HUMAN REVIEW'}")
    if a.release and errors: raise SystemExit(1)
