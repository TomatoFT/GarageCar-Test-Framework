# Page Object Model Guide

## What is POM?

Each page (or major UI area) gets a Python class that holds:

1. **Locators** — how to find elements
2. **Actions** — what a user does (click, fill, navigate)

Tests call page methods and keep **assertions** in the test file.

## Rules used in this framework

| Do | Don't |
|----|-------|
| Put `expect(...)` in tests | Put assertions in page methods (except rare helpers) |
| Name methods by user intent (`login`, `open`) | Name methods by mechanics (`click_submit_btn`) |
| Use `get_by_role` / `get_by_label` | Rely on long CSS paths |
| One page class per logical screen | One class per URL fragment |

## Example flow

```
test_login.py          →  login_page.login()  →  DashboardPage
test_reception.py      →  reception_page.open() →  table visible
test_dashboard.py      →  sidebar.go_to_reception()
```

## Components vs pages

- **Page** — full screen (`LoginPage`, `DashboardPage`)
- **Component** — fragment reused across pages (`Sidebar`)

See [components/sidebar.py](../components/sidebar.py).

## Fluent navigation (optional pattern)

`LoginPage.login()` returns `DashboardPage` so you can chain:

```python
dashboard = login_page.open().login("opera", "1")
```

This is optional — returning `self` or nothing is also fine for simple tests.
