# Test Pyramid — GarageCar + This Framework

```
        /\
       /  \     E2E (qa-framework) — few, slow, high confidence
      /----\
     /      \   Integration — Django views, DB
    /--------\
   /          \ Unit — services.py business logic
  /--------------\
```

## GarageCar unit tests (`~/GarageCar/tests/`)

| File | What it tests |
|------|----------------|
| `test_payment_services.py` | Payment validation, debt updates |
| `test_repair_services.py` | Labor line debt increment |
| `test_reception_services.py` | Daily reception limits |
| `test_core_services.py` | Business rule seeding |
| `test_views.py` | Auth guards on views |

Run: `cd ~/GarageCar && pytest -v`

These tests hit **services and views directly** — no browser, very fast.

## This framework E2E tests (`~/qa-framework/tests/`)

| Folder | What it tests |
|--------|----------------|
| `tests/ui/` | Real user flows in Chromium |
| `tests/api/` | HTTP endpoints with session auth |
| `tests/visual/` | Screenshot regression |

Run: `cd ~/qa-framework && pytest -m smoke`

## When to add which?

| Scenario | Layer |
|----------|-------|
| Debt cannot exceed vehicle balance | Unit (`GarageCar`) |
| Login form redirects to dashboard | E2E UI (`qa-framework`) |
| Search API returns JSON shape | API (`qa-framework`) |
| Kanban drag updates status | E2E UI (exercise for you) |

**Rule of thumb:** push logic tests down the pyramid; use E2E for critical user journeys only.
