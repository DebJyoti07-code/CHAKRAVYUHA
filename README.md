# CHAKRAVYUHA
### AI-Powered Threat Intelligence & Forensic Investigation Platform

CHAKRAVYUHA is an AI-assisted cybersecurity platform that analyzes suspicious URLs, detects potential phishing indicators, and provides actionable security insights through multi-layer threat investigation.

## 1. Problem

With the increasing number of phishing attacks and fraudulent websites, users often struggle to identify whether a link or website is safe.

Traditional security tools may provide basic warnings but do not always explain the potential risks or suggest what users should do next.

This creates a need for a platform that can analyze suspicious links, identify security indicators, and present understandable investigation results.

## 2. Solution

CHAKRAVYUHA provides an AI-assisted threat investigation system that evaluates suspicious URLs through multiple security checks.

Key features include:

- **URL Analysis:** Extracts and analyzes submitted URLs.
- **Phishing Indicators:** Identifies suspicious website characteristics.
- **Domain Intelligence:** Retrieves domain registration information using WHOIS.
- **TLS Analysis:** Checks website SSL/TLS certificates.
- **Website Inspection:** Examines security headers and website content.
- **Infrastructure Checks:** Checks selected network services.
- **AI Investigation:** Generates threat verdicts and damage control recommendations.
- **Community Reporting:** Stores reports of suspicious domains.
- **Risk Scoring:** Calculates a trust score based on identified risk indicators.
- **Scan History:** Displays previously recorded scan results.

## 3. Demo Links and Screenshot

- **Live Demo:** [Add your deployed project link]
- **Demo Video:** [Add your demo video link]
- **GitHub Repository:** [Add your GitHub repository link]

### Project Screenshot

Add a screenshot of the working CHAKRAVYUHA dashboard here.

`![CHAKRAVYUHA Dashboard](screenshots/dashboard.png)`

## 4. Tech Stack

| Category | Technologies |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| UI Framework | Tailwind CSS |
| Charts | Chart.js |
| Icons | Font Awesome |
| Backend | Python, FastAPI |
| Database | MongoDB Atlas |
| AI Integration | Groq API, GPT-OSS-20B |
| HTTP Client | HTTPX |
| HTML Parsing | BeautifulSoup |
| Domain Intelligence | WHOIS |
| Security Analysis | SSL, Socket |
| Async Processing | Asyncio |
| API Communication | REST API, JSON |

## 5. Architecture

CHAKRAVYUHA follows a three-layer Client–Server Architecture.

**1. Presentation Layer**
- HTML, CSS and JavaScript
- Tailwind CSS
- Chart.js
- Handles user interaction and displays investigation results.

**2. Application Layer**
- Python and FastAPI
- URL processing and security analysis
- Risk score calculation
- Groq API integration for AI-generated insights

**3. Data Layer**
- MongoDB Atlas
- `recent_scans` collection
- `community_flags` collection

### Workflow

User Input → URL Extraction → Security Analysis → Risk Assessment → AI Investigation → Result Dashboard → Database Storage

## 6. Setup and Run Steps

### Prerequisites

- Python 3.10 or later
- MongoDB Atlas account
- Groq API key
- VS Code or another code editor

### Step 1: Clone the Repository

```bash
git clone <your-github-repository-link>
cd CHAKRAVYUHA
```

### Step 2: Install Dependencies

```bash
pip install fastapi uvicorn httpx motor beautifulsoup4 python-whois
```

### Step 3: Configure Environment Variables

Configure your MongoDB connection URI and Groq API key securely through environment variables. Update the backend to read these values instead of keeping credentials inside the source code.

### Step 4: Run the Backend

```bash
uvicorn main:app --reload
```

Replace `main` with your actual backend Python filename if it is different.

### Step 5: Open the Frontend

Open the frontend `index.html` file in your browser and ensure the backend API is running.

## 7. Disclosures (Libraries, Templates, AI Tools)

### Libraries and Frameworks
- FastAPI – Backend API development.
- Tailwind CSS – Frontend styling.
- Chart.js – Data visualization.
- Font Awesome – Icons.
- HTTPX – HTTP communication.
- Motor – Asynchronous MongoDB integration.
- BeautifulSoup – HTML parsing.
- WHOIS – Domain registration information.

### AI Tools and Services
- Groq API – AI inference service.
- GPT-OSS-20B – AI model used for investigation summaries and recommendations.
- GitHub Copilot – AI-assisted coding support, if used during development.

### External Resources
- Tailwind CSS CDN
- Chart.js CDN
- Font Awesome CDN

All third-party libraries and services are credited to their respective developers and providers.

## 8. Track

**Selected Track:** [Add your actual hackathon track here]

## 9. Project Status

CHAKRAVYUHA is currently a working prototype demonstrating AI-assisted threat investigation.

Some components, including threat intelligence data and historical analytics, currently use demonstration logic and can be expanded through future integrations.

### Future Scope
- Integration with real-time threat intelligence databases.
- Advanced phishing and brand impersonation detection.
- Browser extension for real-time URL protection.
- Improved machine learning-based threat detection.
- Expanded community-driven threat intelligence.

---

**CHAKRAVYUHA — Turning Suspicious Links into Actionable Intelligence.** 
