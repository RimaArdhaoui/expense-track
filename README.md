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


- [ ] Export scan results into a `reports/` folder for your writeup
