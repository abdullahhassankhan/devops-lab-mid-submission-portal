
# DevOps Lab Mid — Assignment Submission Portal

**COMSATS University Islamabad, Attock Campus**

**Course:** DevOps for Cloud Computing (CSC418)  
**Student:** Abdullah Hassan Khan  
**Registration Number:** FA23-BAI-062

## 1. Project Overview

This project implements a web-based Assignment Submission Portal using Python, Flask, and SQLite. It demonstrates continuous integration, automated testing, GitHub Actions, and automatic delivery of test reports to a local computer.

The project was developed for the DevOps Lab Mid assessment. It also includes a GitHub Pages deployment and automatic CI email notifications.

### Key Features

- Student assignment submission form
- Required-field and submission URL validation
- Persistent SQLite database storage in the local Flask application
- Display of saved submissions
- Automated testing with Pytest
- GitHub Actions CI pipeline triggered on pushes and pull requests
- Automated JUnit XML test report generation
- Local HTTP test report receiver
- Secure report delivery through Cloudflare Tunnel
- Automatic local JSON report generation
- Passing, failing, and corrected CI pipeline demonstrations
- Static GitHub Pages frontend with browser-local submission storage
- Conditional GitHub Pages deployment after successful CI
- Automatic email reporting for passing and failing CI runs

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11 | Application development and report automation |
| Flask | Web application and HTTP report receiver |
| SQLite | Persistent submission storage in the Flask application |
| HTML, CSS, and JavaScript | Web interface and static GitHub Pages frontend |
| Browser localStorage | Browser-local submissions on the static demonstration site |
| Pytest | Automated testing |
| Git and GitHub | Version control and repository hosting |
| GitHub Actions | Continuous integration, email reporting, and deployment |
| GitHub Pages | Hosting the static demonstration website |
| Cloudflare Tunnel | HTTPS connectivity to the local report receiver |
| JSON and JUnit XML | Automated test reporting |
| Gmail SMTP | Automated CI email notifications |

## 3. Project Structure

| Path | Purpose |
|---|---|
| `app/__init__.py` | Flask application, validation, and database logic |
| `app/templates/index.html` | Flask assignment submission interface |
| `app/static/style.css` | Flask frontend styling |
| `site/index.html` | Static GitHub Pages submission interface |
| `site/style.css` | GitHub Pages styling |
| `site/script.js` | Client-side validation and browser-local submissions |
| `tests/test_portal.py` | Automated Pytest test cases |
| `receiver/server.py` | Authenticated local HTTP report receiver |
| `receiver/send_report.py` | CI test report parser and JSON sender |
| `receiver/send_email.py` | CI email report sender |
| `.github/workflows/ci.yml` | CI, reporting, and deployment workflow |
| `run.py` | Flask application entry point |
| `requirements.txt` | Python dependencies |
| `reports/` | Local test reports generated at runtime |
| `evidence/` | Screenshots of CI, reporting, deployment, and email results |
| `.gitignore` | Exclusion rules for local and sensitive files |

## 4. Installation and Setup

### Clone the Repository

```powershell
git clone https://github.com/abdullahhassankhan/devops-lab-mid-submission-portal.git
cd devops-lab-mid-submission-portal
```

### Create a Python Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, configure the current session and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

## 5. Run the Assignment Submission Portal

Start the Flask application:

```powershell
python run.py
```

Open the following address:

http://127.0.0.1:5000

The portal allows students to submit their name, registration number, assignment title, and a valid HTTP or HTTPS submission URL.

Valid submissions are stored in the local SQLite database and displayed in the **Saved Submissions** table.

## 6. Execute Automated Tests

Run the complete test suite:

```powershell
python -m pytest -v tests
```

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
8. Send the automated CI email report on push events.
9. Deploy the static site to GitHub Pages following a successful test job on `main` pushes.

The report delivery step runs after both successful and failed tests.

The email step is configured to attempt delivery even when tests fail. Email-sending errors are not configured to fail the CI job.

The GitHub Pages deployment is conditional on the `automated-tests` job succeeding.

### GitHub Actions

https://github.com/abdullahhassankhan/devops-lab-mid-submission-portal/actions

## 8. Local HTTP Report Receiver

The local receiver is implemented in:

`receiver/server.py`

Start it in a separate terminal:

```powershell
python receiver/server.py
```

The receiver listens on:

http://127.0.0.1:5050

### Health Check Endpoint

`GET /health`

http://127.0.0.1:5050/health

### Report Submission Endpoint

`POST /report`

The receiver requires a private authentication token supplied through the `Authorization` header.

If `.report-token` does not exist, generate a secure token before starting the receiver.

The token must remain private and must never be committed to GitHub.

Valid received reports are automatically saved to:

`reports/test-report.json`

The report contains:

- Repository information
- Branch name
- Commit SHA
- GitHub Actions workflow run ID
- Execution timestamp
- Individual test results
- Failure messages when applicable
- Overall test summary

## 9. Cloudflare Tunnel Configuration

The GitHub-hosted runner cannot access the local computer through its own `localhost` address.

Cloudflare Tunnel provides an HTTPS connection to the local report receiver.

### Start Cloudflare Tunnel

With the `cloudflared` client installed, start a temporary tunnel:

```powershell
cloudflared tunnel --url http://127.0.0.1:5050
```

The generated HTTPS address forwards requests to the local receiver.

### GitHub Actions Secrets

Configure the following repository secrets:

| Secret | Description |
|---|---|
| `REPORT_RECEIVER_URL` | Current HTTPS tunnel URL ending in `/report` |
| `REPORT_RECEIVER_TOKEN` | Private authentication token matching the local receiver |

Both the local receiver and tunnel must remain running during report delivery.

Quick Tunnel URLs are temporary and may change when restarted.

Update the GitHub repository secret whenever the tunnel URL changes.

The token and local database are excluded from Git using `.gitignore`.

**Important:** If the workflow cannot reach the receiver, the report-delivery step may fail and prevent the dependent Pages deployment.

Confirm that the receiver, tunnel, and secret URL are available when running the full pipeline.

## 10. Automatic JSON Test Reporting

The script `receiver/send_report.py` reads actual Pytest JUnit XML results generated during CI.

It prepares a JSON report containing:

- Repository, branch, commit SHA, run ID, and execution timestamp
- Individual test names and results
- Failure messages for failed tests
- Total, passed, failed, and skipped test counts
- Overall execution status

The report is sent through an authenticated HTTP POST request to the local receiver.

The receiver automatically creates or updates:

`reports/test-report.json`

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

### Core CI Evidence

- `evidence/01_initial_passing_ci.png`
- `evidence/02_failing_ci.png`
- `evidence/03_corrected_passing_ci.png`
- `evidence/04_local_json_passing.png`
- `evidence/05_local_json_failing.png`

## 12. Security Considerations

- Virtual environment files are excluded from Git.
- The SQLite database is stored locally.
- The private `.report-token` file is excluded from Git.
- Authentication is required for report submissions.
- GitHub Actions credentials are stored in repository secrets.
- HTTPS is used for external report delivery.
- Gmail App Passwords and authentication tokens are not stored in source code.
- Public evidence screenshots should not expose credentials or private account details.
- The local receiver and temporary tunnel should only run when required.

## 13. Repository

**GitHub Repository:**

https://github.com/abdullahhassankhan/devops-lab-mid-submission-portal

**Branch:** `main`

**Project:** DevOps Lab Mid — Assignment Submission Portal

## 14. Bonus Feature 1 — GitHub Pages Deployment

The project includes an automated GitHub Pages deployment pipeline integrated with GitHub Actions.

### Live Website

https://abdullahhassankhan.github.io/devops-lab-mid-submission-portal/

### Features

- Responsive HTML and CSS frontend
- Assignment submission form
- Client-side JavaScript validation
- Browser `localStorage` for demonstration submissions
- Saved submissions table
- Automatic deployment after successful CI tests
- Deployment prevention when CI tests fail

GitHub Pages hosts the **static demonstration frontend**.

The original Flask application and SQLite database remain separate from the deployed static website.

Data entered on the static website is stored in the current browser.

It is **not** stored in the Flask application's SQLite database or shared across browsers.

### Conditional Deployment

The deployment job is defined in:

`.github/workflows/ci.yml`

It uses:

- `needs: automated-tests`
- Deployment restricted to pushes on `main`
- GitHub Pages deployment actions

The website is deployed only when the `automated-tests` job succeeds.

If CI tests fail, GitHub Pages deployment is skipped and the previously published website remains available.

### Demonstration Results

| Stage | Result |
|---|---|
| Initial successful deployment | Passed |
| Intentional failing CI run | Deployment skipped |
| Restored passing CI run | Deployment successful |

### Evidence

- `evidence/06_pages_successful_deployment.png`
- `evidence/07_pages_deployment_skipped.png`

This demonstrates automated deployment and CI-based deployment gating.

## 15. Bonus Feature 2 — Automatic Email Reporting

The project implements automatic CI email reporting using Python, Gmail SMTP, and GitHub Actions.

### Implementation

**Email sender:**

`receiver/send_email.py`

The email script reads actual Pytest JUnit XML results and sends a formatted report through Gmail SMTP.

### Email Contents

Each email includes:

- Repository name
- Branch name
- Commit SHA
- GitHub Actions run ID
- Overall CI status
- Total test count
- Number of passed and failed tests
- Individual test results
- Failure messages when applicable
- GitHub Actions workflow link

### Secure SMTP Configuration

The following GitHub Actions Secrets are used:

| Secret | Purpose |
|---|---|
| `SMTP_USERNAME` | Gmail SMTP account username |
| `SMTP_PASSWORD` | Gmail App Password for SMTP authentication |
| `REPORT_EMAIL` | Recipient address for CI reports |

`SMTP_PASSWORD` contains the Gmail App Password.

Credentials are never stored directly in source code.

The email report is sent automatically on push-triggered workflow runs and covers both passing and failing tests.

### Automated Email Demonstration

| Stage | Result |
|---|---|
| Successful CI run | `CI PASSED` email received |
| Intentional failing CI run | `CI FAILED` email received |
| Final corrected CI run | `CI PASSED` email received |

The last verified successful email was for commit:

`56c7297`

### Evidence

- `evidence/08_email_passing.png`
- `evidence/09_email_failing.png`

This demonstrates automated email notification for both successful and failed CI executions.

## 16. Final Project Verification

The project successfully demonstrates:

1. Flask Assignment Submission Portal
2. SQLite database integration
3. Automated Pytest validation
4. GitHub Actions CI pipeline
5. Authenticated automatic JSON report delivery
6. Passing, failing, and corrected CI demonstrations
7. Conditional GitHub Pages deployment
8. Automatic passing and failing email notifications

### Last Verified CI Status

| Field | Result |
|---|---|
| Last Verified Commit | `56c7297` |
| Workflow Run Number | `12` |
| Total Tests | 3 |
| Passed | 3 |
| Failed | 0 |
| GitHub Pages | Deployed successfully |
| Email Reporting | Delivered successfully |

These results describe the last verified workflow run.

Updating this README creates a new commit and a new CI run, which should be checked separately before submission.

All core and optional bonus features have been implemented and demonstrated.

Final grading remains subject to instructor evaluation.

---

**Developed by:** Abdullah Hassan Khan  
**Registration Number:** FA23-BAI-062  
**Course:** CSC418 — DevOps for Cloud Computing  
**Institution:** COMSATS University Islamabad, Attock Campus
