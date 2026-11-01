
"use strict";

// DevOps Lab Mid - GitHub Pages Static Demo

const STORAGE_KEY = "devops_lab_mid_submissions";

const form = document.getElementById("submission-form");
const message = document.getElementById("message");
const submissionList = document.getElementById("submission-list");
const emptyState = document.getElementById("empty-state");


// Display success or validation messages
function showMessage(text, type) {
    message.textContent = text;
    message.className = type;
}


// Validate HTTP / HTTPS URLs
function isValidURL(value) {
    try {
        if (!value || /\s/.test(value)) {
            return false;
        }

        const url = new URL(value);

        return (
            (url.protocol === "http:" ||
             url.protocol === "https:") &&
            Boolean(url.hostname)
        );

    } catch (error) {
        return false;
    }
}


// Retrieve saved submissions
function getSubmissions() {
    const stored = localStorage.getItem(STORAGE_KEY);

    if (!stored) {
        return [];
    }

    const parsed = JSON.parse(stored);

    return Array.isArray(parsed) ? parsed : [];
}


// Save submissions in browser storage
function saveSubmissions(submissions) {
    localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify(submissions)
    );
}


// Display all saved submissions
function displaySubmissions() {
    submissionList.replaceChildren();

    const submissions = getSubmissions();

    emptyState.hidden = submissions.length > 0;

    submissions.forEach((submission) => {
        const row = document.createElement("tr");

        // Student Name
        const nameCell = document.createElement("td");
        nameCell.textContent = submission.student_name;

        // Registration Number
        const registrationCell = document.createElement("td");
        registrationCell.textContent =
            submission.registration_number;

        // Assignment Title
        const assignmentCell = document.createElement("td");
        assignmentCell.textContent =
            submission.assignment_title;

        // Submission Link
        const linkCell = document.createElement("td");

        if (isValidURL(submission.submission_url)) {
            const link = document.createElement("a");

            link.href = submission.submission_url;
            link.textContent = "View Submission";
            link.target = "_blank";
            link.rel = "noopener noreferrer";

            linkCell.appendChild(link);
        } else {
            linkCell.textContent = "Invalid link";
        }

        row.append(
            nameCell,
            registrationCell,
            assignmentCell,
            linkCell
        );

        submissionList.appendChild(row);
    });
}


// Handle assignment submission
form.addEventListener("submit", function (event) {
    event.preventDefault();

    const studentName =
        document.getElementById("student_name").value.trim();

    const registrationNumber =
        document.getElementById("registration_number").value.trim();

    const assignmentTitle =
        document.getElementById("assignment_title").value.trim();

    const submissionURL =
        document.getElementById("submission_url").value.trim();

    // Required fields validation
    if (!studentName) {
        showMessage("Student Name is required.", "error");
        return;
    }

    if (!registrationNumber) {
        showMessage("Registration Number is required.", "error");
        return;
    }

    if (!assignmentTitle) {
        showMessage("Assignment Title is required.", "error");
        return;
    }

    if (!submissionURL) {
        showMessage("Submission URL is required.", "error");
        return;
    }

    // URL validation
    if (!isValidURL(submissionURL)) {
        showMessage(
            "Please enter a valid HTTP or HTTPS URL.",
            "error"
        );
        return;
    }

    // Prepare new submission
    const newSubmission = {
        student_name: studentName,
        registration_number: registrationNumber,
        assignment_title: assignmentTitle,
        submission_url: submissionURL
    };

    try {
        // Save valid submission
        const submissions = getSubmissions();

        submissions.push(newSubmission);
        saveSubmissions(submissions);

        // Refresh saved submissions table
        displaySubmissions();

        // Clear form after successful submission
        form.reset();

        showMessage(
            "Assignment submitted successfully!",
            "success"
        );

    } catch (error) {
        showMessage(
            "Unable to save submission. Check browser storage.",
            "error"
        );
        console.error("Storage error:", error);
    }
});


// Load submissions when page opens
try {
    displaySubmissions();
} catch (error) {
    showMessage(
        "Unable to load saved submissions.",
        "error"
    );
    console.error("Storage error:", error);
}
