#!/bin/sh
set -e
python -c "
from app import create_app
from app.db import init_db
app = create_app()
with app.app_context():
    init_db()
"
exec gunicorn -b 0.0.0.0:5000 "app:create_app()"
