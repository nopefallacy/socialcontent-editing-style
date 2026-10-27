#!/usr/bin/env bash
# Contact sheet of chosen moments from a render, for the quality gates (references/06).
#   scripts/sheet.sh renders/draft.mp4 out.jpg 1.7 8.9 11.15 32.1 ...     (3 columns, 640px tiles)
set -euo pipefail
video="$1"; out="$2"; shift 2
tmp="$(mktemp -d)"
n=0
for t in "$@"; do
  ffmpeg -v error -y -ss "$t" -i "$video" -frames:v 1 -vf "scale=640:-1" "$tmp/$(printf %03d $n).png"
  n=$((n + 1))
done
rows=$(( (n + 2) / 3 ))
ffmpeg -v error -y -i "$tmp/%03d.png" -frames:v 1 -vf "tile=3x${rows}" "$out"
rm -rf "$tmp"
echo "$out ($n frames: $*)"
