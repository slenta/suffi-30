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

    # Vercel Postgres endpoint — pin the specific project host, NOT a wildcard.
    # Wildcards (*.vercel-storage.com) are silently dropped by dig at init.
    # Get the host from `vercel env pull` → POSTGRES_URL → strip credentials.
    # TODO: replace with the project's actual ep-<hash>.<region>.postgres.vercel-storage.com
    "ep-REPLACE-WITH-PROJECT-HOST.us-east-1.postgres.vercel-storage.com"
)

EXTRA_IPS=(
    # Vercel public anycast — covers production frontends, default preview URLs
    # (<hash>.vercel.app), and most platform endpoints. Stable; published by
    # Vercel for firewall allowlisting.
    "76.76.21.0/24"
)

source /usr/local/lib/firewall-base.sh
