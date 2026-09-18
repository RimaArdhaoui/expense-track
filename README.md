# Ledger — a tiny expense tracker

A small Flask app: register, log in, add/filter/delete personal
expenses, plus a `/api/expenses` JSON endpoint. Built to be a real
(if minimal) codebase to run a DevSecOps pipeline against for the
Phase 1 (Development) lab — not a toy "hello world."

## Run it locally

```bash
python -m venv .venv
source .venv/bin/activate      # on the Ubuntu VM
pip install -r requirements.txt
flask --app app init-db
python run.py
```

Then open http://127.0.0.1:5000

## Run the tests

```bash
pytest -q
```

## Project layout

```
app/
  __init__.py      # app factory
  config.py        # SECRET_KEY / DATABASE config
  db.py            # sqlite schema + connection helpers
  routes.py        # all routes: auth, dashboard, expenses, search, API
  templates/        # Jinja2 templates
  static/style.css
tests/test_app.py  # pytest suite
.github/workflows/ci.yml   # baseline pipeline (tests only, so far)
```

## Where this fits the lab

This repo is deliberately left at the **"DevOps pipeline done, security
not yet integrated"** stage described in the assignment brief. `ci.yml`
currently only installs dependencies and runs tests — that's your
baseline DevOps chain.

Two things worth knowing before you start the security part:

1. **`app/routes.py` → `search_expenses()`** builds its SQL query with
   plain string formatting instead of a parameterized query — a
   realistic SQL-injection-prone pattern, left in on purpose as a real
   finding for your SAST tool (Semgrep/Bandit) to catch during the
   lab. Fixing it (and showing the before/after) is good material for
   your report.
2. To demonstrate secret-scanning (e.g. Gitleaks) at the pre-commit
   stage, temporarily add a fake credential to a file (e.g. an
   `AKIA...`-style dummy AWS key in a comment or a `.env` file),
   commit, and confirm the hook blocks it — then remove it. Don't
   commit a real credential.

## Next steps (yours to do for the lab)

- [ ] Add a `.pre-commit-config.yaml` with a secret-scanning hook
- [ ] Add a SAST job (e.g. Semgrep) to `.github/workflows/ci.yml`
- [ ] Fix the SQL injection in `search_expenses()` using the flagged
      tool's finding, and document the before/after
- [ ] Export scan results into a `reports/` folder for your writeup
