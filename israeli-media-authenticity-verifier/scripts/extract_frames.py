#!/usr/bin/env python3
"""Build the ffmpeg command that extracts frames for inspection. Launches nothing.

The script validates the options, creates the output folder and prints one
correctly quoted command for you to run. Requires ffmpeg 5.1 or newer, because
-fps_mode replaced the -vsync option that current ffmpeg no longer accepts.

Modes:
  python extract_frames.py <video>                     # 1 frame per second
  python extract_frames.py <video> --fps 2 --out dir
  python extract_frames.py <video> --keyframes         # scene changes
  python extract_frames.py <video> --keyframes --scene-threshold 0.25
  python extract_frames.py <video> --iframes           # stored I-frames only

Use --iframes first on a heavily recompressed WhatsApp forward. A single
continuous shot has no scene cut, so --keyframes can yield no frames and ffmpeg
can exit with an error. Use --iframes or the fixed-rate mode for such a clip.

After extraction, inspect frames with references/artifact-checklist.md for
flicker, identity drift and motion warping. Do not use blinking or lip-sync as a
tell. Reverse-search several clear frames, with any identifiable face cropped or
blurred first, to test for recycled footage.
"""
import argparse
import os
import shlex
import sys


def safe_input(path: str) -> str:
    """Stop a file name that starts with a dash from being read as an ffmpeg option."""
    return path if not path.startswith("-") else os.path.join(".", path)


def build_command(args: argparse.Namespace, pattern: str) -> list:
    video = safe_input(args.video)
    if args.iframes:
        return ["ffmpeg", "-skip_frame", "nokey", "-i", video, "-fps_mode", "vfr", "-y", pattern]
    if args.keyframes:
        select = f"select='gt(scene,{args.scene_threshold})'"
        return ["ffmpeg", "-i", video, "-vf", select, "-fps_mode", "vfr", "-y", pattern]
    return ["ffmpeg", "-i", video, "-vf", f"fps={args.fps}", "-y", pattern]


def main() -> int:
    parser = argparse.ArgumentParser(description="Print the ffmpeg command for frame extraction")
    parser.add_argument("video", help="Path to the video file")
    parser.add_argument("--fps", type=float, default=1.0, help="Frames per second to sample (default 1)")
    parser.add_argument("--out", default="frames", help="Output directory (default ./frames)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--keyframes", action="store_true", help="Select scene-change frames")
    mode.add_argument("--iframes", action="store_true", help="Keep only the stored I-frames")
    parser.add_argument(
        "--scene-threshold",
        type=float,
        default=0.4,
        help="Scene-change score for --keyframes, above 0 and below 1 (default 0.4)",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.video):
        print(f"ERROR: video not found: {args.video}", file=sys.stderr)
        return 1
    if args.fps <= 0:
        print("ERROR: --fps must be above 0.", file=sys.stderr)
        return 1
    if not 0 < args.scene_threshold < 1:
        print("ERROR: --scene-threshold must be above 0 and below 1.", file=sys.stderr)
        return 1

    if args.out.startswith("-") or "%" in args.out:
        print("ERROR: --out must not start with a dash or contain a percent sign.", file=sys.stderr)
        return 1

    os.makedirs(args.out, exist_ok=True)
    if any(name.startswith("frame_") for name in os.listdir(args.out)):
        print(f"WARNING: {args.out} already holds frames, and they may be mixed with this run.", file=sys.stderr)

    pattern = os.path.join(args.out, "frame_%04d.jpg")
    print("Run this command:")
    print(shlex.join(build_command(args, pattern)))
    print(f"\nThen open the frames in {args.out}/ and step through them with references/artifact-checklist.md.")
    print("Look for flicker, identity drift and warping. Do not submit a frame showing an identifiable")
    print("person's face to any reverse-image or visual search engine. Crop or blur faces locally first.")
    print("With --keyframes, a clip with no scene cut gives zero frames and ffmpeg may exit with an error.")
    print("That is not a finding about the clip: use --iframes or the default fixed-rate mode instead.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
