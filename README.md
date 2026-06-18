# QA Framework — Playwright + Python (POM)

A learning-focused end-to-end test framework for [GarageCar](https://github.com/TomatoFT/GarageCar) (Garage Pro).

## Quick start

```bash
# 1. Bootstrap the demo app (one-time)
chmod +x scripts/setup_app.sh
./scripts/setup_app.sh

# 2. Install this framework
cd ~/qa-framework
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install
cp .env.example .env

# 3. Start GarageCar (separate terminal)
cd ~/GarageCar && source .venv/bin/activate && python manage.py runserver

# 4. Run tests
pytest -m smoke -v
```

**Demo login:** `opera` / `1` at http://127.0.0.1:8000/login/

## Project layout

```
pages/          Page Object Model — locators + user actions
components/     Reusable UI fragments (sidebar, etc.)
tests/ui/       Browser E2E tests
tests/api/      HTTP API tests (faster layer)
tests/visual/   Screenshot regression
data/           External test data (JSON)
docs/           SDET learning guides
```

## Core business flow tests

End-to-end coverage of the garage loop:

| Test file | Flow |
|-----------|------|
| `test_reception_wizard.py` | 4-step intake wizard |
| `test_repair_flow.py` | Start repair + add labor + Kanban |
| `test_payment_flow.py` | Collect + confirm payment |
| `test_core_flow.py` | Full reception → repair → payment |

```bash
pytest -m regression -v    # includes core flow tests
pytest tests/ui/test_core_flow.py -v
```

**Prerequisite:** run `./scripts/setup_app.sh` then start `runserver` *after* setup (so labor rates load in repair forms).

| Command | Purpose |
|---------|---------|
| `pytest -m smoke` | Critical path (CI default) |
| `pytest -m regression` | Broader UI coverage |
| `pytest -m api` | API tests only |
| `pytest -m negative` | Validation / boundary failures |
| `pytest -m visual --update-baselines` | Refresh visual baselines |
| `pytest --headed --slowmo 500` | Watch tests run in slow motion |
| `pytest --html=reports/report.html` | HTML report |
| `./scripts/run_tests.sh` | Wait for server + run smoke |
| `./scripts/docker-test.sh` | Docker: app + full test suite |

## SDET features

| Feature | Location |
|---------|----------|
| **storageState** (fast auth) | `tests/conftest.py` → `auth_storage` |
| **Negative tests** | `tests/ui/test_negative.py` |
| **Shared flows** | `tests/helpers/garage_flow.py` |
| **Docker Compose** | `docker-compose.yml` |
| **CI smoke + nightly regression** | `.github/workflows/playwright.yml` |

## Test pyramid

| Layer | Where | Run with |
|-------|-------|----------|
| Unit / service | `GarageCar/tests/` | `cd ~/GarageCar && pytest` |
| E2E (this repo) | `qa-framework/tests/` | `pytest -m smoke` |

## CI and the two-repo setup

This framework lives in **qa-framework**. The app under test is **[GarageCar](https://github.com/TomatoFT/GarageCar)** — a separate repo.

### How CI works today

| Question | Answer |
|----------|--------|
| Where is the workflow file? | Only here: [`.github/workflows/playwright.yml`](.github/workflows/playwright.yml) |
| What triggers CI? | Push/PR to **qa-framework**, nightly schedule (02:00 UTC), or manual **Run workflow** |
| Does a GarageCar push/PR trigger this CI? | **No** |
| Does CI test the app? | **Yes** — it clones GarageCar, starts Django, runs Playwright |
| Which GarageCar code is tested? | Always `TomatoFT/GarageCar` **default branch** (`master`), not a GarageCar PR branch |

```text
qa-framework PR/push  ──►  CI runs  ──►  clone GarageCar (master)  ──►  pytest
GarageCar PR/push     ──►  (nothing in this repo)
```

### CI jobs

| Job | When | Command | Artifacts |
|-----|------|---------|-----------|
| `smoke` | Every push / PR to qa-framework | `pytest -m smoke` | `smoke-report` (HTML, traces, screenshots) |
| `regression` | Nightly + manual only | `pytest -m regression` | `regression-report` |

Each job:

1. Checks out **qa-framework** (the commit that triggered the run)
2. Checks out **GarageCar** from GitHub (`path: GarageCar`)
3. Migrates DB, seeds business rules, creates demo user
4. Runs [`scripts/seed_e2e_data.py`](scripts/seed_e2e_data.py) (Toyota brand + labor rate)
5. Starts `python manage.py runserver`
6. Runs pytest and uploads reports

Download failed-run artifacts from **GitHub → Actions → Playwright E2E → job → Artifacts**.

### Local vs CI

| | Local | CI |
|---|-------|-----|
| App source | Your `~/GarageCar` clone | Fresh clone of `master` each run |
| Test source | Your working tree | qa-framework commit that triggered CI |
| `GARAGE_DIR` | `~/GarageCar` (default) | `$GITHUB_WORKSPACE/GarageCar` |

### The gap (important for real projects)

Because CI only runs when **qa-framework** changes:

- A breaking change merged to **GarageCar** will **not** fail this pipeline automatically.
- CI never tests a **GarageCar PR branch** — only `master`.

That is fine for a learning repo. For production, teams usually add one of:

1. **Workflow in GarageCar** — run E2E on every app PR (tests the PR branch).
2. **Cross-repo trigger** — GarageCar dispatches a workflow in qa-framework.
3. **Monorepo** — app + tests in one repository.

### Run CI locally (same stack as Actions)

```bash
# Option 1: against your local GarageCar
./scripts/setup_app.sh
cd ~/GarageCar && source .venv/bin/activate && python manage.py runserver
cd ~/qa-framework && pytest -m smoke -v

# Option 2: Docker (clones nothing — uses GARAGE_DIR volume)
export GARAGE_DIR=~/GarageCar
./scripts/docker-test.sh
```

Manual regression (matches nightly job):

```bash
pytest -m regression --browser chromium \
  --html=reports/regression-report.html \
  --self-contained-html \
  --tracing retain-on-failure \
  --screenshot only-on-failure
```

More detail: [docs/CI_AND_DEBUGGING.md](docs/CI_AND_DEBUGGING.md)

## Learn more

- [docs/LEARNING_PATH.md](docs/LEARNING_PATH.md) — ordered SDET curriculum
- [docs/POM_GUIDE.md](docs/POM_GUIDE.md) — Page Object Model patterns
- [docs/TEST_PYRAMID.md](docs/TEST_PYRAMID.md) — unit vs E2E
- [docs/CI_AND_DEBUGGING.md](docs/CI_AND_DEBUGGING.md) — traces, CI artifacts

## Note on login URL

GarageCar settings reference `/accounts/login/` but the working route is `/login/`. This framework uses `/login/` (see `.env`).
