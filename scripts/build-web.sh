#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# UME prompt ("Ready to start !") is kept enabled because browser autoplay
# policy needs a real user gesture before audio can play. Without it the
# console fires a play() error on load until the player first clicks.
exec uv run pygbag --ume_block 1 --build .
