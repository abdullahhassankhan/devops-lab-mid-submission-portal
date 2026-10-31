
import sqlite3
from pathlib import Path
from urllib.parse import urlsplit

from flask import Flask, render_template, request, redirect, url_for


def is_valid_url(url):
    if not url or any(char.isspace() for char in url):
        return False

    try:
        parsed = urlsplit(url)
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.hostname)
            and (parsed.port is None or parsed.port > 0)
        )
    except ValueError:
        return False


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["DATABASE_PATH"] = str(
        Path(app.instance_path) / "submissions.db"
    )

    if test_config:
        app.config.update(test_config)

    db_path = Path(app.config["DATABASE_PATH"])
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Create database table
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                registration_number TEXT NOT NULL,
                assignment_title TEXT NOT NULL,
                submission_url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    @app.route("/", methods=["GET", "POST"])
    def home():
        errors = []

        fields = {
            "student_name": "Student Name",
            "registration_number": "Registration Number",
            "assignment_title": "Assignment Title",
            "submission_url": "Submission URL",
        }

        values = {key: "" for key in fields}

        if request.method == "POST":
            values = {
                key: request.form.get(key, "").strip()
                for key in fields
            }

            # Required fields validation
            for key, label in fields.items():
                if not values[key] and key != "registration_number":
                    errors.append(f"{label} is required.")

            # URL validation
            if values["submission_url"]:
                if not is_valid_url(values["submission_url"]):
                    errors.append("Please enter a valid HTTP or HTTPS URL.")

            if not errors:
                with sqlite3.connect(db_path) as conn:
                    conn.execute("""
                        INSERT INTO submissions
                        (student_name, registration_number,
                         assignment_title, submission_url)
                        VALUES (?, ?, ?, ?)
                    """, (
                        values["student_name"],
                        values["registration_number"],
                        values["assignment_title"],
                        values["submission_url"],
                    ))

                return redirect(url_for("home", saved="1"))

        # Load saved submissions
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            submissions = [
                dict(row) for row in conn.execute(
                    "SELECT * FROM submissions ORDER BY id DESC"
                ).fetchall()
            ]

        return render_template(
            "index.html",
            submissions=submissions,
            errors=errors,
            values=values,
            saved=request.args.get("saved") == "1",
        ), (400 if errors else 200)

    return app
