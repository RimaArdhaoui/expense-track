import functools
from datetime import date

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint("app", __name__)


# ---------- auth ----------

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.get("user") is None:
            return redirect(url_for("app.login"))
        return view(**kwargs)
    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        error = None

        if not username or not password:
            error = "Username and password are required."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."

        db = get_db()
        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                flash("Account created — please log in.")
                return redirect(url_for("app.login"))

        flash(error)

    return render_template("register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if user is None or not check_password_hash(user["password_hash"], password):
            error = "Incorrect username or password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("app.dashboard"))

        flash(error)

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("app.login"))


# ---------- expenses ----------

@bp.route("/")
@login_required
def dashboard():
    db = get_db()
    expenses = db.execute(
        "SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC",
        (g.user["id"],),
    ).fetchall()
    total = sum(row["amount"] for row in expenses)
    return render_template("dashboard.html", expenses=expenses, total=total)


@bp.route("/expenses/add", methods=("POST",))
@login_required
def add_expense():
    amount = request.form.get("amount")
    category = request.form.get("category", "").strip()
    note = request.form.get("note", "").strip()

    error = None
    try:
        amount = float(amount)
        if amount <= 0:
            error = "Amount must be positive."
    except (TypeError, ValueError):
        error = "Amount must be a number."
    if not category:
        error = "Category is required."

    if error:
        flash(error)
    else:
        db = get_db()
        db.execute(
            "INSERT INTO expenses (user_id, amount, category, note, date) "
            "VALUES (?, ?, ?, ?, ?)",
            (g.user["id"], amount, category, note, date.today().isoformat()),
        )
        db.commit()

    return redirect(url_for("app.dashboard"))


@bp.route("/expenses/<int:expense_id>/delete", methods=("POST",))
@login_required
def delete_expense(expense_id):
    db = get_db()
    db.execute(
        "DELETE FROM expenses WHERE id = ? AND user_id = ?",
        (expense_id, g.user["id"]),
    )
    db.commit()
    return redirect(url_for("app.dashboard"))


@bp.route("/expenses/search")
@login_required
def search_expenses():
    category = request.args.get("category", "")
    db = get_db()
    expenses = db.execute(
        "SELECT * FROM expenses WHERE user_id = ? AND category LIKE ? ORDER BY date DESC",
        (g.user["id"], f"%{category}%"),
    ).fetchall()
    total = sum(row["amount"] for row in expenses)
    return render_template(
        "dashboard.html", expenses=expenses, total=total, search=category
    )

# ---------- simple JSON API ----------

@bp.route("/api/expenses")
@login_required
def api_expenses():
    db = get_db()
    expenses = db.execute(
        "SELECT id, amount, category, note, date FROM expenses WHERE user_id = ?",
        (g.user["id"],),
    ).fetchall()
    return jsonify([dict(row) for row in expenses])
