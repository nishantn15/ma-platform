#!/data/data/com.termux/files/usr/bin/bash
# Render a Hyperframes composition on Termux/Android.
# Hyperframes node_modules must live on ext4 (~/ma-video-workspace), not /sdcard
# (FAT has no symlinks). This script syncs the repo's Video/ compositions into
# the workspace, renders, and copies the MP4 back into Video/renders/.
#
# Usage: ./render.sh <composition-dir> [hyperframes render flags...]
#   e.g. ./render.sh brand-film --quality high --fps 30
set -euo pipefail

REPO_VIDEO="/storage/emulated/0/Download/MidMarket_MA_Platform_TK/Video"
WS="$HOME/ma-video-workspace"
COMP="${1:?usage: render.sh <composition-dir> [flags]}"; shift || true

# Hyperframes-on-Android env (see memory: hyperframes-termux)
export NODE_OPTIONS="--require $WS/hf-platform-shim.cjs"
export HYPERFRAMES_BROWSER_PATH=/data/data/com.termux/files/usr/bin/chromium-browser
export PRODUCER_HEADLESS_SHELL_PATH=/data/data/com.termux/files/usr/bin/chromium-browser
export PUPPETEER_SKIP_DOWNLOAD=1

# Sync composition source into the workspace (ext4) for rendering
mkdir -p "$WS/$COMP" "$REPO_VIDEO/renders"
cp -r "$REPO_VIDEO/$COMP/." "$WS/$COMP/"

cd "$WS/$COMP"
OUT="$REPO_VIDEO/renders/$COMP.mp4"
echo "▶ Rendering $COMP → $OUT"
npx --yes hyperframes@0.6.97 render --no-browser-gpu -w 1 -o "$OUT" "$@"
echo "✓ $OUT"
ls -lh "$OUT"
