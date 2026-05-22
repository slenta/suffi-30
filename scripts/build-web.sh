#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

# --ume_block 0 skips pygbag's "Ready to start !" click prompt.
# Browser autoplay policy still requires a real user gesture before audio
# plays — pygbag handles that with retry semantics on first interaction.
exec uv run pygbag --ume_block 0 --build .
