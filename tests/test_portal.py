
import sqlite3

import pytest

from app import create_app


@pytest.fixture
def test_setup(tmp_path):
    """Create an isolated Flask app and temporary database."""
    database_path = tmp_path / "test_submissions.db"

    app = create_app({
        "TESTING": True,
        "DATABASE_PATH": str(database_path),
    })

    with app.test_client() as client:
        yield client, database_path


def count_submissions(database_path):
    """Return the number of saved submissions."""
    with sqlite3.connect(database_path) as conn:
        result = conn.execute(
            "SELECT COUNT(*) FROM submissions"
        ).fetchone()

    return result[0]


# TEST CASE 1: Valid submission
def test_valid_submission(test_setup):
    client, database_path = test_setup

    response = client.post("/", data={
        "student_name": "Abdullah Hassan Khan",
        "registration_number": "FA23-BAI-062",
        "assignment_title": "DevOps Lab Mid",
        "submission_url": "https://github.com/abdullahhassankhan",
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Assignment submitted successfully!" in response.data
    assert b"Abdullah Hassan Khan" in response.data
    assert b"FA23-BAI-062" in response.data
    assert count_submissions(database_path) == 1


# TEST CASE 2: Missing registration number
def test_missing_registration_number(test_setup):
    client, database_path = test_setup

    response = client.post("/", data={
        "student_name": "Abdullah Hassan Khan",
        "registration_number": "",
        "assignment_title": "DevOps Lab Mid",
        "submission_url": "https://github.com/abdullahhassankhan",
    })

    assert response.status_code == 400
    assert b"Registration Number is required." in response.data
    assert count_submissions(database_path) == 0


# TEST CASE 3: Invalid submission URL
def test_invalid_submission_url(test_setup):
    client, database_path = test_setup

    response = client.post("/", data={
        "student_name": "Abdullah Hassan Khan",
        "registration_number": "FA23-BAI-062",
        "assignment_title": "DevOps Lab Mid",
        "submission_url": "invalid-url-123",
    })

    assert response.status_code == 400
    assert b"Please enter a valid HTTP or HTTPS URL." in response.data
    assert count_submissions(database_path) == 0
