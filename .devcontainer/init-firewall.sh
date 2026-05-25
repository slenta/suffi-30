#!/bin/bash
# Per-repo firewall domains for suffi-30 (pygbag + Vercel + Neon Postgres).

EXTRA_DOMAINS=(
    # Vercel
    "vercel.com"
    "api.vercel.com"
    "*.vercel.com"
    "*.vercel.app"
    # Pygbag CDN (pythons.js, cpython312/main.js, archives/repo)
    "pygame-web.github.io"
    "raw.githubusercontent.com"
    # Pygbag pulls additional Python wheels from PyPI at runtime
    "pypi.org"
    "files.pythonhosted.org"
    # Neon Postgres (matches POSTGRES_URL host pattern)
    "*.neon.tech"
    "*.aws.neon.tech"
)
source /usr/local/lib/firewall-base.sh
