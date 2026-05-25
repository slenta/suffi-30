#!/bin/bash
# Per-repo firewall domains for suffi-30 (pygbag + Vercel + Vercel Postgres).

EXTRA_DOMAINS=(
    # Vercel platform — docs/dashboard are Cloudflare-fronted (covered by base);
    # API endpoint pinned explicitly.
    "vercel.com"
    "api.vercel.com"

    # This project's own Vercel deployment (e.g. /api/highscores endpoint).
    # Resolves to anycast pools outside 76.76.21.0/24 (observed: 64.29.17.x,
    # 216.198.79.x). If those IPs rotate and connections start failing,
    # rebuild the container to re-resolve.
    "suffi-30.vercel.app"

    # Pygbag CDN (pythons.js, cpython312/main.js, archives/repo)
    "pygame-web.github.io"
    "raw.githubusercontent.com"

    # Pygbag pulls additional Python wheels from PyPI at runtime
    # (the base allowlist already covers pypi.org + files.pythonhosted.org)

    # Neon Postgres endpoint (pooler). Pin the specific host, NOT a wildcard —
    # *.aws.neon.tech is silently dropped by dig at init. Get the host from
    # the Neon console → Connect → Pooled connection string.
    "ep-muddy-snow-ag4i5uf0-pooler.c-2.eu-central-1.aws.neon.tech"
)

EXTRA_IPS=(
    # Vercel public anycast — covers production frontends, default preview URLs
    # (<hash>.vercel.app), and most platform endpoints. Stable; published by
    # Vercel for firewall allowlisting.
    "76.76.21.0/24"
)

source /usr/local/lib/firewall-base.sh
