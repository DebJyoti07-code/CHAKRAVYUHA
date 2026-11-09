# CHAKRAVYUHA
**AI-Powered Threat Intelligence & Forensic Investigation Platform**

## 1. Problem
- Increasing phishing attacks and fake websites.
- Users struggle to identify suspicious links.
- Lack of clear risk analysis and safety guidance.

## 2. Solution
CHAKRAVYUHA analyzes suspicious URLs using multiple security checks and AI-generated insights.

- URL and phishing analysis
- Domain and SSL/TLS checks
- Website security inspection
- Risk score generation
- AI-based threat verdict
- Damage control recommendations
- Community reporting and scan history

## 3. Demo Links and Screenshot
- **Live Demo:** [Add Link]
- **Demo Video:** [Add Link]
- **GitHub:** [Add Link]

**Screenshot:**

![CHAKRAVYUHA Dashboard](screenshots/dashboard.png)

## 4. Tech Stack

- **Frontend:** HTML, CSS, JavaScript, Tailwind CSS
- **Backend:** Python, FastAPI
- **Database:** MongoDB Atlas
- **AI:** Groq API, GPT-OSS-20B
- **Libraries:** Chart.js, Font Awesome, HTTPX, Motor, BeautifulSoup, WHOIS

## 5. Architecture

**Three-Layer Client–Server Architecture**

1. **Presentation:** HTML, CSS, JavaScript
2. **Application:** Python, FastAPI, AI integration
3. **Data:** MongoDB Atlas

**Workflow:** User Input → URL Analysis → Risk Assessment → AI Investigation → Results

## 6. Setup and Run Steps

```bash
git clone <repository-link>
cd CHAKRAVYUHA
pip install fastapi uvicorn httpx motor beautifulsoup4 python-whois
uvicorn main:app --reload
```

Open `index.html` in your browser.

Configure MongoDB URI and Groq API key using environment variables.

## 7. Disclosures

- **Libraries:** Tailwind CSS, Chart.js, Font Awesome, FastAPI, HTTPX, Motor, BeautifulSoup.
- **AI Service:** Groq API with GPT-OSS-20B.
- **AI Coding Tool:** GitHub Copilot (if used).
- **External Resources:** Third-party libraries via CDN.

## 8. Track
hackmatrix 
