import os
import sqlite3
from datetime import date, timedelta
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-demo-secret")

# On Render, set DATABASE_PATH to a directory on a persistent disk if desired.
# Example: /var/data/medicines.db (after attaching a disk mounted at /var/data).
DEFAULT_DB = Path(__file__).resolve().parent / "medicines.db"
DB_PATH = Path(os.environ.get("DATABASE_PATH", str(DEFAULT_DB)))
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def connect_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with connect_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                batch TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                expiry_date TEXT NOT NULL
            )
        """)


def get_status(expiry_string):
    expiry = date.fromisoformat(expiry_string)
    today = date.today()
    if expiry < today:
        return "Expired"
    if expiry <= today + timedelta(days=30):
        return "Expiring Soon"
    return "Safe"


@app.route("/")
def dashboard():
    search = request.args.get("q", "").strip()
    with connect_db() as db:
        all_rows = db.execute("SELECT * FROM medicines ORDER BY expiry_date").fetchall()
        if search:
            rows = db.execute(
                """SELECT * FROM medicines
                   WHERE name LIKE ? OR batch LIKE ?
                   ORDER BY expiry_date""",
                (f"%{search}%", f"%{search}%"),
            ).fetchall()
        else:
            rows = all_rows

    counts = {"Safe": 0, "Expiring Soon": 0, "Expired": 0}
    medicines = []
    for row in all_rows:
        counts[get_status(row["expiry_date"])] += 1
    for row in rows:
        item = dict(row)
        item["status"] = get_status(item["expiry_date"])
        medicines.append(item)

    return render_template(
        "index.html",
        medicines=medicines,
        total=len(all_rows),
        safe=counts["Safe"],
        soon=counts["Expiring Soon"],
        expired=counts["Expired"],
        query=search,
        today=date.today().isoformat(),
    )


@app.route("/add", methods=["POST"])
def add_medicine():
    name = request.form.get("name", "").strip()
    batch = request.form.get("batch", "").strip()
    expiry_date = request.form.get("expiry_date", "").strip()
    quantity_raw = request.form.get("quantity", "").strip()

    try:
        quantity = int(quantity_raw)
        parsed_expiry = date.fromisoformat(expiry_date)
        if not name or not batch or quantity < 1:
            raise ValueError
    except ValueError:
        flash("Please enter a name, batch, valid expiry date and quantity greater than zero.", "error")
        return redirect(url_for("dashboard"))

    with connect_db() as db:
        db.execute(
            "INSERT INTO medicines (name, batch, quantity, expiry_date) VALUES (?, ?, ?, ?)",
            (name, batch, quantity, parsed_expiry.isoformat()),
        )
    flash(f"{name} was added to the inventory.", "success")
    return redirect(url_for("dashboard"))


@app.route("/delete/<int:medicine_id>", methods=["POST"])
def delete_medicine(medicine_id):
    with connect_db() as db:
        db.execute("DELETE FROM medicines WHERE id = ?", (medicine_id,))
    flash("Medicine record deleted.", "success")
    return redirect(url_for("dashboard"))


@app.route("/health")
def health():
    return {"status": "ok"}


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
