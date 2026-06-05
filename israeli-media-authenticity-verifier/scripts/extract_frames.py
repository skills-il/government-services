#!/usr/bin/env python3
"""Extract frames from a video so the agent can inspect them one by one.

Video deepfakes and recycled clips reveal themselves frame by frame: temporal
flicker, identity drift across frames, unnatural blinking, lip-sync drift, and
warping around a moving subject. Pull frames, then look at them with the
artifact checklist (references/artifact-checklist.md).

The earliest, clearest frame is also the best input for a reverse-image search
to test the "recycled / miscaptioned real footage" hypothesis.

Requires ffmpeg (macOS): brew install ffmpeg

Usage:
  python extract_frames.py <video>                 # 1 frame per second to ./frames
  python extract_frames.py <video> --fps 2 --out ./frames
  python extract_frames.py <video> --keyframes     # extract only scene-change keyframes
"""
import argparse
import os
import shutil
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract video frames via ffmpeg")
    parser.add_argument("video", help="Path to the video file")
    parser.add_argument("--fps", type=float, default=1.0, help="Frames per second to sample (default 1)")
    parser.add_argument("--out", default="frames", help="Output directory (default ./frames)")
    parser.add_argument(
        "--keyframes",
        action="store_true",
        help="Extract scene-change keyframes instead of a fixed rate",
    )
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        print(
            "ffmpeg not found.\n"
            "Install it with: brew install ffmpeg  (macOS)\n"
            "or your platform package manager.",
            file=sys.stderr,
        )
        return 3

    os.makedirs(args.out, exist_ok=True)
    pattern = os.path.join(args.out, "frame_%04d.jpg")

    if args.keyframes:
        # Select frames where a large scene change occurs (scene score above 0.4).
        vf = "select='gt(scene,0.4)'"
        cmd = ["ffmpeg", "-i", args.video, "-vf", vf, "-vsync", "vfr", "-y", pattern]
    else:
        cmd = ["ffmpeg", "-i", args.video, "-vf", f"fps={args.fps}", "-y", pattern]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        return 1

    frames = sorted(f for f in os.listdir(args.out) if f.startswith("frame_"))
    print(f"Extracted {len(frames)} frames to {args.out}/")
    print(
        "Next: open the frames and step through them with"
        " references/artifact-checklist.md.\nLook for flicker, identity drift,"
        " blink cadence, lip-sync drift, and warping. Reverse-search the clearest"
        " frame to test for recycled / miscaptioned footage."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
