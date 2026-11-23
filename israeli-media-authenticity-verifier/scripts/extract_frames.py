#!/usr/bin/env python3
"""Print the ffmpeg command that extracts frames for inspection. Launches nothing.

Run the printed command, then look at the frames with the artifact checklist
(references/artifact-checklist.md) for flicker, identity drift and motion warping.

The earliest, clearest frame is also the best input for a reverse-image search
(with any identifiable face cropped or blurred first)
to test the "recycled / miscaptioned real footage" hypothesis.

Requires ffmpeg 5.1 or newer (macOS): brew install ffmpeg

Usage:
  python extract_frames.py <video>                 # 1 frame per second to ./frames
  python extract_frames.py <video> --fps 2 --out ./frames
  python extract_frames.py <video> --keyframes     # extract only scene-change keyframes
"""
import argparse
import os
import shlex
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

    if not os.path.isfile(args.video):
        print(f"ERROR: video not found: {args.video}", file=sys.stderr)
        return 1
    if args.fps <= 0:
        print("ERROR: --fps must be above 0.", file=sys.stderr)
        return 1
    if args.out.startswith("-") or "%" in args.out:
        print("ERROR: --out must not start with a dash or contain a percent sign.", file=sys.stderr)
        return 1

    os.makedirs(args.out, exist_ok=True)
    video = args.video if not args.video.startswith("-") else os.path.join(".", args.video)
    pattern = os.path.join(args.out, "frame_%04d.jpg")

    if args.keyframes:
        # Select frames where a large scene change occurs (scene score above 0.4).
        vf = "select='gt(scene,0.4)'"
        cmd = ["ffmpeg", "-i", video, "-vf", vf, "-fps_mode", "vfr", "-y", pattern]
    else:
        cmd = ["ffmpeg", "-i", video, "-vf", f"fps={args.fps}", "-y", pattern]

    print("Run this command:")
    print(shlex.join(cmd))
    print(f"\nThen step through the frames in {args.out}/ with references/artifact-checklist.md.")
    print("Look for flicker, identity drift and warping. Do not submit a frame showing an identifiable")
    print("person's face to any reverse-image or visual search engine. Crop or blur faces locally first.")
    print("With --keyframes, a clip with no scene cut gives zero frames and ffmpeg may exit with an")
    print("error. That is not a finding about the clip: use the default fixed-rate mode instead.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
