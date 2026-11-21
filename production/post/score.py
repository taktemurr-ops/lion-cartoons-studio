#!/usr/bin/env python3
"""Generate an original short non-vocal cartoon score for production testing.

Pure Python, deterministic WAV; no external music samples or copyrighted melodies.
This is a proof of the automated sound-assembly path, NOT final studio audio.
"""
import argparse
import math
import struct
import wave
from pathlib import Path

RATE = 24000
NOTES = [392.00, 493.88, 587.33, 523.25, 440.00, 392.00, 349.23, 392.00]
def score(t):
    beat = int(t * 3.2)
    note = NOTES[beat % len(NOTES)]
    phase = t * 2 * math.pi
    onset = (t * 3.2) % 1.0
    envelope = (1.0 - onset) ** 1.5
    melody = (math.sin(note * phase) * .55 +
              math.sin(note * phase * 2) * .14 +
              math.sin(note * phase * .5) * .17) * envelope
    bass_note = [196.0, 174.61, 220.0, 196.0][int(t / 1.25) % 4]
    bass = math.sin(bass_note * phase) * .11
    # Lightweight original soft percussion, not an existing sample
    tick = math.sin(2 * math.pi * 920 * t) * (.018 if onset < .07 else 0)
    return .38 * (melody + bass + tick)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seconds", type=float, default=3.0)
    p.add_argument("--output", default="output/original_score.wav")
    a = p.parse_args()
    if not 0 < a.seconds <= 600:
        p.error("seconds must be between 0 and 600")
    dest = Path(a.output)
    dest.parent.mkdir(parents=True, exist_ok=True)
    n = int(a.seconds * RATE)
    fade = min(int(.22 * RATE), n // 8)
    with wave.open(str(dest), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(RATE)
        batch = bytearray()
        for i in range(n):
            fadein = min(1.0, i / max(1, fade))
            fadeout = min(1.0, (n - 1 - i) / max(1, fade))
            amp = max(-1, min(1, score(i / RATE) * fadein * fadeout))
            batch += struct.pack("<h", int(amp * 32767))
            if len(batch) >= 64_000:
                f.writeframesraw(batch); batch.clear()
        if batch: f.writeframesraw(batch)
    print(f"WAV created: {dest} ({a.seconds}s)")

if __name__ == "__main__":
    main()
