# TalentMatch AI - Enterprise Job Fit Analyzer



## 1. Project Overview & Business Value
TalentMatch AI is an intelligent "Smart Job Board" screening tool designed to optimize HR recruitment pipelines. Standard Applicant Tracking Systems (ATS) rely on rigid keyword matching, which often filters out highly qualified candidates. 

This application utilizes the Google Gemini 3.5 Flash Large Language Model (LLM) to contextually analyze a candidate's uploaded resume (PDF) against a specific Job Description. 

**Core Business Value:**
*   **Automated Screening:** Instantly evaluates candidate viability, drastically reducing manual HR screening hours.
*   **Skill Gap Analysis:** Generates concrete matching skills and highlights critical missing requirements.
*   **Fraud Detection (Authenticity Score):** Evaluates if the resume reads like a genuine professional document or contains stuffed/fake keywords.
*   **Data-Driven Decisions:** Outputs an objective Match Percentage score to help recruiters rank candidates systematically.

## 2. Technical Architecture & Tech Stack
The application is built using a modern, scalable, and serverless stack:
*   **Frontend UI:** HTML5, Responsive Tailwind CSS (CDN), Vanilla JavaScript with the Fetch API.
*   **Backend Framework:** Python 3.10 with Flask.
*   **AI Integration:** Direct HTTP REST integration with Google Generative AI (Gemini 3.5 Flash) via the `requests` library. Prompt engineering enforces strict JSON output.
*   **File Processing:** `PyPDF2` for robust text extraction from uploaded PDF resumes in memory.
*   **Hosting & Serverless Runtime:** Deployed on Vercel using the `@vercel/python` serverless runtime engine.

## 3. Features
*   **Drag-and-Drop Upload:** Professional UI supporting direct PDF resume uploads (multipart/form-data).
*   **Enterprise-Grade Backend:** Includes secure environment variable management via `python-dotenv`, comprehensive logging, and robust error handling.
*   **Strict JSON Parsing:** The backend reliably parses AI-generated text into valid JSON for the frontend to consume, sanitizing Markdown delimiters automatically.
*   **Interactive UI:** Dynamic animations for match scores and visual badges for skills.

## 4. CI/CD Pipeline Implementation
Deployment is entirely automated using Continuous Integration and Continuous Deployment (CI/CD) via GitHub Actions. 
*   **Workflow File:** `.github/workflows/deploy.yml`
*   **Trigger:** Automatically triggers on a `push` to the `main` branch.
*   **Execution:** 
    1. Sets up the Python environment (3.10) and installs the `uv` package manager.
    2. Installs the Vercel CLI.
    3. Securely pulls environment configurations using GitHub Secrets (`VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`, `VERCEL_TOKEN`).
    4. Builds the project artifacts and deploys seamlessly to the Vercel Production environment.

## 5. Local Setup Instructions
To run this project locally for development:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jayeshhsathawane/TalentMatch-AI.git
   cd TalentMatch_AI
