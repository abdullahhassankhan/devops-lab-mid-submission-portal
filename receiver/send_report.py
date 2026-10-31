
import json
import os
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit


REPORT_PATH = Path("reports/junit.xml")


def parse_test_results():
    """Read actual Pytest JUnit XML results."""

    if not REPORT_PATH.exists():
        raise FileNotFoundError(
            "JUnit XML report not found."
        )

    root = ET.parse(REPORT_PATH).getroot()

    tests = []

    for case in root.findall(".//testcase"):

        failure = case.find("failure")
        error = case.find("error")
        skipped = case.find("skipped")

        issue = failure if failure is not None else error

        if issue is not None:
            result = "failed"
            failure_message = (
                issue.get("message")
                or issue.text
                or "Test failed"
            ).strip()

        elif skipped is not None:
            result = "skipped"
            failure_message = None

        else:
            result = "passed"
            failure_message = None

        tests.append({
            "name": case.get("name", "unknown"),
            "result": result,
            "failure_message": failure_message
        })

    total = len(tests)

    if total == 0:
        raise ValueError("No test results found in XML.")

    passed = sum(
        test["result"] == "passed"
        for test in tests
    )

    failed = sum(
        test["result"] == "failed"
        for test in tests
    )

    skipped = sum(
        test["result"] == "skipped"
        for test in tests
    )

    status = (
        "failed" if failed > 0
        else "incomplete" if skipped > 0
        else "passed"
    )

    return tests, {
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "status": status
    }


def send_report():

    receiver_url = os.environ["REPORT_RECEIVER_URL"]
    receiver_token = os.environ["REPORT_RECEIVER_TOKEN"]

    if urlsplit(receiver_url).scheme != "https":
        raise ValueError("HTTPS receiver URL required.")

    tests, summary = parse_test_results()

    report = {
        "repository": os.environ["GITHUB_REPOSITORY"],
        "branch": os.environ["GITHUB_REF_NAME"],
        "commit_sha": os.environ["GITHUB_SHA"],
        "run_id": os.environ["GITHUB_RUN_ID"],
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "tests": tests,
        "summary": summary
    }

    # Keep a local copy within the CI workspace
    output = Path("reports/ci-test-report.json")

    output.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )

    # Send actual test results to receiver
    payload = json.dumps(report).encode("utf-8")

    req = urllib.request.Request(
        receiver_url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {receiver_token}"
        },
        method="POST"
    )

    with urllib.request.urlopen(
        req,
        timeout=30
    ) as response:

        if response.status != 200:
            raise RuntimeError(
                f"Receiver returned HTTP {response.status}"
            )

    print("Test report delivered successfully!")
    print(f"Overall status: {summary['status']}")
    print(f"Total: {summary['total']}")
    print(f"Passed: {summary['passed']}")
    print(f"Failed: {summary['failed']}")


if __name__ == "__main__":
    try:
        send_report()
    except Exception as exc:
        print(
            f"Report delivery failed: {type(exc).__name__}: {exc}",
            file=sys.stderr
        )
        sys.exit(1)
