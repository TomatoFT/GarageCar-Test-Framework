# SDET Learning Path

Follow this order. Each step links to code you can read and a command to run.

## 1. QA fundamentals

**Concepts:** test types, Arrange-Act-Assert, test pyramid.

**Read:** [docs/TEST_PYRAMID.md](TEST_PYRAMID.md)

**Run:**
```bash
cd ~/GarageCar && pytest -v          # app unit tests
cd ~/qa-framework && pytest -m smoke -v   # E2E smoke
```

## 2. Locators

**Concepts:** resilient selectors (`get_by_role`, `get_by_label`) vs brittle CSS.

**Read:** [pages/login_page.py](../pages/login_page.py)

**Run:** `pytest tests/ui/test_login.py --headed`

## 3. Page Object Model

**Concepts:** pages own actions; tests own assertions.

**Read:** [docs/POM_GUIDE.md](POM_GUIDE.md), [pages/reception_page.py](../pages/reception_page.py)

**Run:** `pytest tests/ui/test_reception.py -v`

## 4. Fixtures

**Concepts:** setup/teardown, authenticated state, dependency injection.

**Read:** [tests/conftest.py](../tests/conftest.py) — `authenticated_page`, `api_client`

**Run:** `pytest tests/ui/test_dashboard.py -v`

## 5. Test data

**Concepts:** externalize data, Faker for unique values.

**Read:** [data/users.json](../data/users.json), [utils/helpers.py](../utils/helpers.py)

**Exercise:** Add a negative test using a new row in `users.json`.

## 6. Markers (tags)

**Concepts:** smoke vs regression suites.

**Read:** [pytest.ini](../pytest.ini)

**Run:**
```bash
pytest -m smoke
pytest -m negative          # boundary / validation failures
pytest -m "regression and not visual"
```

## 7. Fast auth with storageState

**Concepts:** session reuse, setup once / run many tests.

**Read:** [tests/conftest.py](../tests/conftest.py) — `auth_storage`, `authenticated_page`

Login runs once per session; cookies saved to `.auth/storage.json`.

## 8. API testing

**Concepts:** faster feedback, JSON contracts, session cookies.

**Read:** [tests/api/test_search_api.py](../tests/api/test_search_api.py)

**Run:** `pytest -m api -v`

## 9. Visual regression

**Concepts:** screenshot baselines, when to use (stable UI only).

**Read:** [tests/visual/test_login_visual.py](../tests/visual/test_login_visual.py)

**Run:**
```bash
pytest -m visual --update-baselines   # first time / after intentional UI change
pytest -m visual                      # compare against baselines/
```

## 10. CI/CD

**Concepts:** headless runs, artifacts, health checks.

**Read:** [.github/workflows/playwright.yml](../.github/workflows/playwright.yml), [docs/CI_AND_DEBUGGING.md](CI_AND_DEBUGGING.md)

## 11. Stretch exercises (build these yourself)

Core flows are implemented in `tests/ui/test_core_flow.py` — read those first, then extend:

| Exercise | URL | Skill |
|----------|-----|-------|
| Parts on repair line | `/repairs/<pk>/lines/<line_pk>/` | Nested page objects |
| Inventory intake | `/inventory/parts/` | Stock management |
| Kanban drag-and-drop | `/repairs/workshop/` | `drag_and_drop` |
| Revenue report | `/reports/revenue/` | Report validation |
| Role-based access | `/accounts/create-staff/` | Admin-only routes |

Use `utils/helpers.py` → `unique_license_plate()` for reception data.
