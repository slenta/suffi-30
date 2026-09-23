#!/bin/bash
# Per-repo firewall domains for suffi-30 (pygbag + Vercel + Neon Postgres).
#
# The base's egress proxy filters by HOST NAME now, not by IP — see
# ~/code/devcontainer-base/docs/security-model.md, "Firewall architecture" and
# "Allowlist entries". EXTRA_IPS (the old IP-allowlist mechanism) is refused
# by the new base: it exits the firewall init with no network at all rather
# than silently dropping the rule, so a repo still setting it finds out at
# once instead of losing egress quietly.

EXTRA_DOMAINS=(
    # Vercel platform. ".vercel.app" (leading dot = the domain + every
    # subdomain) covers both this project's production deploy
    # (suffi-30.vercel.app) and its per-PR preview URLs (<hash>.vercel.app) —
    # those hashes change on every deploy, so a wildcard is the only entry
    # that keeps working. vercel.com/api.vercel.com are the dashboard/API,
    # not the app itself, but the same account used them under the old
    # EXTRA_IPS range.
    ".vercel.app"
    "vercel.com"
    "api.vercel.com"

    # Pygbag CDN (pythons.js, cpython312/main.js, archives/repo)
    "pygame-web.github.io"
    "raw.githubusercontent.com"

    # Pygbag pulls additional Python wheels from PyPI at runtime
    # (the base allowlist already covers pypi.org + files.pythonhosted.org)
)

# github.com over SSH (this repo's origin remote) needs no entry here — the
# base opens :22 to github.com by default for every consumer.

# Neon Postgres (highscores, psycopg2 over POSTGRES_URL) is raw TCP on :5432,
# which the HTTP(S) proxy cannot carry. EXTRA_TCP_HOSTS opens that one port to
# the pooler host; the base re-resolves the name at every container start, so
# Neon moving the endpoint to new IPs is picked up on the next restart.
EXTRA_TCP_HOSTS=(
    "ep-muddy-snow-ag4i5uf0-pooler.c-2.eu-central-1.aws.neon.tech:5432"
)

source /usr/local/lib/firewall-base.sh
