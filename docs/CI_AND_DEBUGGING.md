# CI and Debugging

## Local debugging

```bash
# See the browser (fish shell)
source .venv/bin/activate.fish
pytest tests/ui/test_login.py --headed --slowmo 500

# Bash / zsh
source .venv/bin/activate

# Pause on failure
PWDEBUG=1 pytest tests/ui/test_login.py

# HTML report (open reports/report.html in browser)
pytest -m regression --html=reports/report.html --self-contained-html
```

## Session reuse (`storageState`)

Login runs **once per session** and saves cookies to `.auth/storage.json`.

Tests using `authenticated_page` restore that session — much faster than logging in every test.

Login tests still use the plain `page` fixture (no saved session).

## Docker (reproducible environment)

```bash
chmod +x scripts/docker-test.sh
export GARAGE_DIR=~/GarageCar
./scripts/docker-test.sh
```

Starts GarageCar + runs smoke + regression, writes `reports/report.html`.

## CI (GitHub Actions)

| Job | When | What runs |
|-----|------|-----------|
| `smoke` | Every push / PR | `pytest -m smoke` + HTML report artifact |
| `regression` | Nightly 02:00 UTC + manual | `pytest -m regression` + traces/screenshots |

Download artifacts from the Actions tab when a job fails.

### Manual regression run

GitHub → Actions → Playwright E2E → Run workflow

## Traces and screenshots

```bash
pytest -m regression \
  --tracing retain-on-failure \
  --screenshot only-on-failure
```

Open trace: `playwright show-trace test-results/.../trace.zip`

## Negative tests

```bash
pytest -m negative -v
```

Covers: unknown repair plate, payment over debt, daily reception limit.

## Flaky test hygiene

- Prefer `expect(...)` over `time.sleep()` — Playwright auto-waits
- Use `authenticated_page` (storageState) instead of repeating login
- CI regression job uses `--reruns 1` for transient flakes
- Seed E2E data **before** starting `runserver` so labor rates appear in forms
