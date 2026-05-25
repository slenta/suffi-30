# suffi-30

Pygame platformer compiled to WASM via pygbag, deployed to Vercel with a Neon Postgres-backed highscore API.

## Run the game locally on :8000

If a build already exists in `build/web/`, run:

```bash
python3 scripts/serve-local.py
```

Open http://localhost:8000/. The devcontainer's `appPort: 8000:8000` forwards it to the host.

**Do not use `python -m http.server` here.** Pygbag's runtime fetches Python wheels from same-origin paths like `/archives/repo/cp312/*.whl`, and `vercel.json` rewrites those to `https://pygame-web.github.io/archives/...` in prod. A plain http.server has no rewrite → 404 on the wheels → black screen. `scripts/serve-local.py` replicates that rewrite with a 302 redirect.

**Do not use `python -m pygbag .` either.** It re-packs the full 92 MB asset archive on every launch and then binds to `127.0.0.1` only, which Docker port forwarding cannot reach.

## Rebuild for deploy

```bash
./rebuild_and_deploy.sh    # rm -rf build/ && pygbag --build && vercel --prod
```
