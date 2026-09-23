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

# Neon Postgres (POSTGRES_URL, read by platformer/core/database.py and
# api/highscores.py via psycopg2) is a raw TCP connection on :5432, which the
# HTTP(S) proxy above cannot carry — CONNECT only tunnels :443, plain HTTP
# only :80 (firewall-base.sh, section 6). It needs a narrow iptables allow by
# IP instead, same as the old EXTRA_IPS mechanism, but scoped to this one
# port rather than a whole CIDR.
#
# OPEN QUESTION (flagged for review, not resolved here): Neon pooler
# endpoints are names on rotating infrastructure, not a stable range — unlike
# EXTRA_SSH_HOSTS, this hook has no DNS available (root has none inside
# extra_firewall_setup; see firewall-base.sh's comment on EXTRA_SSH_HOSTS'
# setpriv trick, which only exists for the port-22 case) to re-resolve the
# host at every container start. The three /32s below are what
# ep-muddy-snow-ag4i5uf0-pooler.c-2.eu-central-1.aws.neon.tech resolved to on
# 2026-09-23; if Neon migrates this project's compute to a different node
# these will go stale silently (connections will just start timing out) until
# someone re-resolves and edits this file. Options not taken here: (a) ask
# the base to grow an EXTRA_SSH_HOSTS-style "resolve at init, pin an IP for
# one port" mechanism, or (b) move highscores off raw psycopg2 onto Neon's
# HTTP-based driver, which would tunnel over :443 like any other EXTRA_DOMAINS
# entry and need no carve-out at all — real work either way, not a firewall
# tweak.
extra_firewall_setup() {
    for ip in 63.178.215.242 63.179.28.86 3.69.34.233; do
        iptables -A OUTPUT -m owner --uid-owner node -p tcp -d "$ip" --dport 5432 -j ACCEPT
    done
}

source /usr/local/lib/firewall-base.sh
