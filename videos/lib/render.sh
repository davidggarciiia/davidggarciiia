#!/usr/bin/env bash
# usage: lib/render.sh <episode-dir> <output-name>
set -e
cd "$1"
node ../../.claude/skills/hyperframes/scripts/plugin-cli.mjs render -o "renders/$2.raw.mp4" -w 3 --quiet > build/render.log 2>&1
ffmpeg -v error -y -i "renders/$2.raw.mp4" -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:a aac -b:a 192k "renders/$2.mp4"
rm -f "renders/$2.raw.mp4"
echo "done $2"
