
import json
import hmac
from pathlib import Path

from flask import Flask, request, jsonify

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_FILE = REPORT_DIR / "test-report.json"
TOKEN_FILE = BASE_DIR / ".report-token"

if not TOKEN_FILE.is_file():
    raise RuntimeError(
        "Receiver token is missing. Create .report-token first."
    )

REPORT_TOKEN = TOKEN_FILE.read_text(encoding="utf-8").strip()

app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "service": "DevOps Lab Mid Report Receiver"
    }), 200


@app.route("/report", methods=["POST"])
def receive_report():

    # Authenticate incoming report
    authorization = request.headers.get("Authorization", "")

    if not hmac.compare_digest(
        authorization, f"Bearer {REPORT_TOKEN}"
    ):
        return jsonify({
            "error": "Unauthorized"
        }), 401

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Valid JSON object is required"
        }), 400

    required_fields = [
        "repository",
        "branch",
        "commit_sha",
        "run_id",
        "timestamp",
        "tests",
        "summary"
    ]

    missing = [
        field for field in required_fields
        if field not in data
    ]

    if missing:
        return jsonify({
            "error": "Missing required report fields",
            "missing": missing
        }), 400

    if not isinstance(data["tests"], list):
        return jsonify({
            "error": "tests must be a list"
        }), 400

    if not isinstance(data["summary"], dict):
        return jsonify({
            "error": "summary must be an object"
        }), 400

    required_summary = [
        "total", "passed", "failed", "status"
    ]

    if any(key not in data["summary"] for key in required_summary):
        return jsonify({
            "error": "Incomplete test summary"
        }), 400

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    temp_file = REPORT_DIR / "test-report.tmp"
    temp_file.write_text(
        json.dumps(data, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )
    temp_file.replace(REPORT_FILE)

    print(f"Test report saved: {REPORT_FILE}", flush=True)

    return jsonify({
        "message": "Test report received successfully",
        "saved_to": str(REPORT_FILE)
    }), 200


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5050,
        debug=False
    )
