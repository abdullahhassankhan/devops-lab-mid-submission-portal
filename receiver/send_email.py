
import os
import ssl
import smtplib
import sys

from email.message import EmailMessage
from send_report import parse_test_results


def get_required_env(name):
    """Read required configuration securely."""
    value = os.environ.get(name, "").strip()

    if not value:
        raise ValueError(
            f"Missing required environment variable: {name}"
        )

    return value


def send_email_report():
    """Email actual Pytest results using Gmail SMTP."""

    # Read credentials from GitHub Actions Secrets
    smtp_username = get_required_env("SMTP_USERNAME")
    smtp_password = get_required_env("SMTP_PASSWORD")
    recipient_email = get_required_env("REPORT_EMAIL")

    # Read actual executed test results
    tests, summary = parse_test_results()

    repository = os.environ.get(
        "GITHUB_REPOSITORY", "unknown"
    )

    branch = os.environ.get(
        "GITHUB_REF_NAME", "unknown"
    )

    commit_sha = os.environ.get(
        "GITHUB_SHA", "unknown"
    )

    run_id = os.environ.get(
        "GITHUB_RUN_ID", "unknown"
    )

    server_url = os.environ.get(
        "GITHUB_SERVER_URL", "https://github.com"
    )

    status = summary["status"].upper()

    # Create email content
    lines = [
        "DEVOPS LAB MID - AUTOMATED CI TEST REPORT",
        "=" * 45,
        "",
        f"Repository: {repository}",
        f"Branch: {branch}",
        f"Commit SHA: {commit_sha}",
        f"Pipeline Run ID: {run_id}",
        "",
        f"Overall Status: {status}",
        f"Total Tests: {summary['total']}",
        f"Passed: {summary['passed']}",
        f"Failed: {summary['failed']}",
        f"Skipped: {summary['skipped']}",
        "",
        "INDIVIDUAL TEST RESULTS",
        "-" * 45,
    ]

    for test in tests:
        test_status = test["result"].upper()

        lines.append(
            f"{test['name']}: {test_status}"
        )

        if test["failure_message"]:
            lines.append(
                f"Failure: {test['failure_message']}"
            )

        lines.append("")

    lines.extend([
        "GITHUB ACTIONS RUN",
        f"{server_url}/{repository}/actions/runs/{run_id}",
        "",
        "This report was generated automatically",
        "from executed Pytest results.",
        "",
        "DevOps Lab Mid - CSC418"
    ])

    # Build email
    email = EmailMessage()

    email["From"] = smtp_username
    email["To"] = recipient_email

    email["Subject"] = (
        f"[DevOps Lab Mid] CI {status} "
        f"- Commit {commit_sha[:7]}"
    )

    email.set_content("\n".join(lines))

    # Send email securely via Gmail SMTP
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465,
        context=context,
        timeout=30
    ) as smtp:

        smtp.login(
            smtp_username,
            smtp_password
        )

        smtp.send_message(email)

    print("Email report sent successfully!")
    print(f"CI Status: {status}")
    print(f"Total Tests: {summary['total']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")


if __name__ == "__main__":
    try:
        send_email_report()

    except Exception as error:
        print(
            f"Email reporting failed: "
            f"{type(error).__name__}: {error}",
            file=sys.stderr
        )
        sys.exit(1)
