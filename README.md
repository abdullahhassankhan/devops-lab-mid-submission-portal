# DevOps Lab Mid — Assignment Submission Portal

**COMSATS University Islamabad, Attock Campus**

**Course:** DevOps for Cloud Computing (CSC418)  
**Student:** Abdullah Hassan Khan  
**Registration Number:** FA23-BAI-062

## 1. Project Overview

This project implements a web-based Assignment Submission Portal using Python, Flask, and SQLite. It demonstrates continuous integration, automated testing, GitHub Actions, and automatic delivery of test reports to a local computer.

The project was developed for the DevOps Lab Mid assessment.

### Key Features

- Student assignment submission form
- Required-field and submission URL validation
- Persistent SQLite database storage
- Display of saved submissions
- Automated testing with Pytest
- GitHub Actions CI pipeline triggered on every push
- Automated JUnit XML test report generation
- Local HTTP test report receiver
- Secure report delivery through Cloudflare Tunnel
- Automatic local JSON report generation
- Passing, failing, and corrected CI pipeline demonstrations

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11 | Application development |
| Flask | Web application and HTTP receiver |
| SQLite | Persistent submission storage |
| HTML and CSS | Frontend interface |
| Pytest | Automated testing |
| Git and GitHub | Version control |
| GitHub Actions | Continuous integration |
| Cloudflare Tunnel | Secure HTTPS connectivity to localhost |
| JSON and JUnit XML | Automated test reporting |

## 3. Project Structure

- `app/__init__.py` — Flask application, validation, and database logic
- `app/templates/index.html` — Assignment submission interface
- `app/static/style.css` — Frontend styling
- `tests/test_portal.py` — Automated Pytest test cases
- `receiver/server.py` — Authenticated local HTTP report receiver
- `receiver/send_report.py` — CI test report parser and sender
- `.github/workflows/ci.yml` — GitHub Actions workflow
- `run.py` — Flask application entry point
- `requirements.txt` — Python dependencies
- `reports/` — Local test reports
- `.gitignore` — Excluded local and sensitive files

## 4. Installation and Setup

### Clone the Repository

`git clone https://github.com/abdullahhassankhan/devops-lab-mid-submission-portal.git`

Enter the project directory:

`cd devops-lab-mid-submission-portal`

### Create a Python Virtual Environment

On Windows PowerShell:

`python -m venv .venv`

Activate it:

`.\.venv\Scripts\Activate.ps1`

If PowerShell blocks script execution, configure the current session:

`Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`

Then activate the environment again.

### Install Dependencies

`python -m pip install -r requirements.txt`

## 5. Run the Assignment Submission Portal

Start the Flask application:

`python run.py`

Open the following address:

http://127.0.0.1:5000

The portal allows students to submit their name, registration number, assignment title, and a valid HTTP or HTTPS submission URL.

Valid submissions are stored in SQLite and displayed in the Saved Submissions table.

## 6. Execute Automated Tests

Run the complete test suite:

`python -m pytest -v tests`

### Automated Test Cases

| Test Case | Expected Result |
|---|---|
| Valid submission | Submission is saved and displayed |
| Missing registration number | Submission rejected with validation error |
| Invalid submission URL | Submission rejected and not saved |

All three tests must pass for a successful test stage.

A failing test produces a nonzero Pytest exit code, causing the GitHub Actions test job to fail.

## 7. GitHub Actions CI Pipeline

The continuous integration pipeline is defined in:

`.github/workflows/ci.yml`

The workflow automatically executes on repository pushes and pull requests.

### Pipeline Operations

1. Checkout the repository.
2. Configure Python 3.11.
3. Install project dependencies.
4. Execute automated Pytest tests.
5. Generate a JUnit XML test report.
6. Send actual test results to the authenticated local receiver on push events.
7. Upload test report artifacts to GitHub Actions.

The report delivery step runs after both successful and failed tests.

GitHub Actions workflows can be viewed at:

https://github.com/abdullahhassankhan/devops-lab-mid-submission-portal/actions

## 8. Local HTTP Report Receiver

The local receiver is implemented in:

`receiver/server.py`

Start it in a separate terminal:

`python receiver/server.py`

The receiver listens on:

http://127.0.0.1:5050

Health check endpoint:

http://127.0.0.1:5050/health

Report submission endpoint:

`POST /report`

The receiver requires a private authentication token supplied through the Authorization header.

If `.report-token` does not exist, generate a secure token before starting the receiver. The token must remain private and must never be committed to GitHub.

Valid received reports are automatically saved to:

`reports/test-report.json`

The report contains repository information, branch, commit SHA, workflow run ID, timestamp, individual test results, failure messages where applicable, and the overall test summary.

## 9. Cloudflare Tunnel Configuration

The GitHub-hosted runner cannot access the local computer using its own `localhost` address.

Cloudflare Tunnel provides an HTTPS connection to the local report receiver.

Install the `cloudflared` client and start a temporary tunnel:

`cloudflared tunnel --url http://127.0.0.1:5050`

The generated HTTPS address forwards requests to the local receiver.

### GitHub Actions Secrets

Configure the following repository secrets:

| Secret | Description |
|---|---|
| `REPORT_RECEIVER_URL` | Current HTTPS tunnel URL ending in `/report` |
| `REPORT_RECEIVER_TOKEN` | Private authentication token matching the local receiver |

Both the local receiver and tunnel must remain running during report delivery.

Quick Tunnel URLs are temporary and may change when restarted. Update the GitHub repository secret whenever the tunnel URL changes.

The token and local database are excluded from Git using `.gitignore`.

## 10. Automatic JSON Test Reporting

The script `receiver/send_report.py` reads actual Pytest JUnit XML results generated during the CI workflow.

It prepares a JSON report containing:

- Repository, branch, commit SHA, run ID, and execution timestamp
- Individual test names and results
- Failure messages for failed tests
- Total, passed, failed, and skipped test counts
- Overall execution status

The report is sent through an authenticated HTTP POST request to the local receiver.

The receiver automatically creates or updates `reports/test-report.json`.

This process supports both passing and failing test runs without manually downloading or copying the report.

## 11. CI Pipeline Demonstration

The following three-stage demonstration was completed:

| Stage | Commit | Passed | Failed | Status |
|---|---|---|---|---|
| Initial Passing Run | `a46fedb` | 3 | 0 | Passed |
| Intentional Defect | `b19f9e2` | 2 | 1 | Failed |
| Corrected Run | `50d1908` | 3 | 0 | Passed |

### Initial Passing Run

All three tests passed, and the JSON report was automatically received on the local computer.

### Intentional Failing Run

An intentional defect was introduced into registration number validation.

The automated test detected that a submission without a registration number was incorrectly accepted.

The pipeline failed, and the local JSON report recorded one failed test with its actual failure message.

### Corrected Passing Run

The original registration validation was restored.

All three tests passed again, and the automatically received JSON report returned to a successful status.

These demonstrations show that the CI workflow detects application defects and delivers actual test results for both successful and unsuccessful executions.

## 12. Security Considerations

- Virtual environment files are excluded from Git.
- The SQLite database is stored locally.
- The private `.report-token` file is excluded from Git.
- Authentication is required for report submissions.
- GitHub Actions credentials are stored in repository secrets.
- HTTPS is used for external report delivery.
- The local receiver and temporary tunnel should only be running when required.

## 13. Repository

**GitHub Repository:**

https://github.com/abdullahhassankhan/devops-lab-mid-submission-portal

**Branch:** `main`

**Project:** DevOps Lab Mid — Assignment Submission Portal

---

**Developed by:** Abdullah Hassan Khan  
**Registration Number:** FA23-BAI-062  
**Course:** CSC418 — DevOps for Cloud Computing  
**Institution:** COMSATS University Islamabad, Attock Campus
