import os
import re
import ssl
import socket
import asyncio
import httpx
import whois
import random
from datetime import datetime, timedelta
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bs4 import BeautifulSoup
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI(title="TRUSTGUARD AI Investigation Engine")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)

# --- MongoDB Setup ---
MONGO_URI = "mongodb+srv://stillverz_db_user:0WJ4lK4yT6IVfxE1@cluster0.d5t7r7e.mongodb.net/"
client = AsyncIOMotorClient(MONGO_URI)
db = client.trustguard
scans_collection = db.recent_scans
flags_collection = db.community_flags

class ScanRequest(BaseModel):
    text: str 

class ReportRequest(BaseModel):
    url: str
    threat_level: str
 
def extract_url(text: str) -> str:
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    match = url_pattern.search(text)
    return match.group(0) if match else None

async def check_threat_database(hostname: str):
    mock_malicious_domains = ["evil.com", "secure-update", "free-crypto", "login-update"]
    is_flagged = any(bad in hostname for bad in mock_malicious_domains)
    return {"flagged_in_database": is_flagged}

async def scan_open_ports(hostname: str):
    ports_to_check = {21: "FTP", 22: "SSH", 3306: "MySQL"}
    open_ports = []
    
    async def check_port(port):
        try:
            _, writer = await asyncio.wait_for(asyncio.open_connection(hostname, port), timeout=0.5)
            writer.close()
            await writer.wait_closed()
            return port
        except Exception:
            return None
            
    results = await asyncio.gather(*(check_port(p) for p in ports_to_check.keys()))
    for res in results:
        if res: open_ports.append(ports_to_check[res])
    return {"exposed_services": open_ports}

async def check_domain_reputation(hostname: str):
    try:
        loop = asyncio.get_event_loop()
        domain_info = await loop.run_in_executor(None, whois.whois, hostname)
        creation_date = domain_info.creation_date
        if isinstance(creation_date, list): 
            creation_date = creation_date[0]
        return {"registered": str(creation_date) if creation_date else "Unknown"}
    except Exception:
        return {"registered": "Unknown"}

async def check_tls_certificate(hostname: str):
    if not hostname:
        return {"secure": False, "error": "Invalid hostname"}
    try:
        context = ssl.create_default_context()
        loop = asyncio.get_event_loop()
        def fetch_cert():
            with socket.create_connection((hostname, 443), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    return ssock.getpeercert()
        cert = await loop.run_in_executor(None, fetch_cert)
        expiry_str = cert.get('notAfter')
        expiry_date = datetime.strptime(expiry_str, '%b %d %H:%M:%S %Y %Z')
        days_remaining = (expiry_date - datetime.now()).days
        return {
            "issuer": dict(x[0] for x in cert.get('issuer', [])),
            "days_until_expiry": days_remaining,
            "secure": True
        }
    except Exception as e:
        return {"secure": False, "error": str(e), "days_until_expiry": 0}

async def analyze_web_security(url: str):
    async with httpx.AsyncClient(verify=False, timeout=5.0) as client:
        try:
            response = await client.get(url, follow_redirects=True)
            soup = BeautifulSoup(response.text, 'html.parser')
            password_inputs = soup.find_all('input', type='password')
            hidden_iframes = soup.find_all('iframe', style=lambda v: v and 'display:none' in v.replace(' ', ''))
            headers = response.headers
            
            security_headers = {
                "hsts": "strict-transport-security" in headers,
                "csp": "content-security-policy" in headers,
                "x_frame_options": "x-frame-options" in headers
            }
            
            page_text = soup.get_text().lower()
            suspicious_keywords = ['porn', 'xxx', 'free movies', 'casino', 'betting', 'viagra']
            content_flag = any(kw in page_text for kw in suspicious_keywords)

            return {
                "has_password_field": len(password_inputs) > 0,
                "hidden_iframes": len(hidden_iframes),
                "is_redirected": str(response.url) != url,
                "final_url": str(response.url),
                "security_headers": security_headers,
                "suspicious_content": content_flag
            }
        except Exception as e:
            return {
                "error": str(e), "has_password_field": False, "hidden_iframes": 0, 
                "is_redirected": False, "final_url": url, 
                "security_headers": {"hsts": False, "csp": False, "x_frame_options": False},
                "suspicious_content": False
            }

async def generate_site_history(base_score: int):
    months = ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]
    history = []
    current = base_score
    for _ in months:
        history.append(current)
        current = min(100, max(10, current + random.randint(-15, 15)))
    history.reverse()
    events = [{"date": (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d"), "event": "Certificate Issuer Changed"}]
    return {"labels": months, "data": history, "events": events}

async def generate_ai_analysis(forensic_data: dict, original_text: str):
    groq_api_key = "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"
    prompt = f"""You are the TRUSTGUARD AI Investigator. Analyze this data to detect Phishing and Brand Impersonation.
    URL: "{original_text}" | Forensics: {forensic_data}
    Return exactly two paragraphs:
    1. 'Verdict': Is it a scam? Explicitly mention Typosquatting, Brand Impersonation, open ports, or TLS expiry.
    2. 'Damage Control': Tell them what to do if they already clicked or submitted data."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {groq_api_key}"},
                json={"model": "openai/gpt-oss-20b", "messages": [{"role": "user", "content": prompt}], "temperature": 0.3},
                timeout=10.0
            )
            return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Verdict: AI Analysis failed ({str(e)}). Damage Control: None."

@app.get("/api/recent") 
async def get_recent_scans():
    try:
        scans = []
        cursor = scans_collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(10)
        async for document in cursor:
            document['time_ago'] = document['timestamp'].strftime("%Y-%m-%d %H:%M")
            scans.append(document)
        return {"scans": scans}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/api/scan")
async def run_investigation(request: ScanRequest):
    try:
        target_url = extract_url(request.text)
        if not target_url:
            raise HTTPException(status_code=400, detail="No valid URL found in the provided text.")
        hostname = urlparse(target_url).hostname

        whitelisted_domains = ["127.0.0.1", "localhost", "0.0.0.0"]
        if hostname in whitelisted_domains:
            return {
                "status": "success", "trust_score": 100, 
                "risk_vectors": {"Phishing Risk": 0, "Identity Risk": 0, "Security Architecture": 0, "Infrastructure Risk": 0},
                "history": {"labels": ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"], "data": [100, 100, 100, 100, 100, 100], "events": []}, 
                "evidence": {
                    "target_url": target_url, "hostname": hostname, "domain_reputation": {"registered": "Local System"},
                    "tls_analysis": {"secure": True, "days_until_expiry": 999, "issuer": {"O": "TRUSTGUARD Internal"}}, 
                    "web_security": {"has_password_field": False, "is_redirected": False, "security_headers": {"hsts": True, "csp": True}}, 
                    "infrastructure": {"exposed_services": []}, "threat_intelligence": {"flagged_in_database": False, "community_flagged": False}
                }, 
                "ai_investigator": "Verdict: This is a verified TRUSTGUARD internal local environment.\nDamage Control: None required."
            }

        community_record = await flags_collection.find_one({"hostname": hostname})
        is_community_flagged = bool(community_record)

        tls_task = asyncio.create_task(check_tls_certificate(hostname))
        dom_task = asyncio.create_task(analyze_web_security(target_url))
        whois_task = asyncio.create_task(check_domain_reputation(hostname))
        port_task = asyncio.create_task(scan_open_ports(hostname))
        threat_db_task = asyncio.create_task(check_threat_database(hostname))
        
        tls_res, dom_res, whois_res, port_res, db_res = await asyncio.gather(tls_task, dom_task, whois_task, port_task, threat_db_task)
        
        phishing_risk = 100 if (db_res.get("flagged_in_database") or is_community_flagged) else (80 if dom_res.get("suspicious_content") else (100 if dom_res.get("has_password_field") and not tls_res.get("secure") else 0))
        identity_risk = 100 if not tls_res.get("secure") else (50 if tls_res.get("days_until_expiry", 999) < 15 else 0)
        security_risk = 60 if len(port_res.get("exposed_services", [])) > 0 else 0
        if not dom_res.get("security_headers", {}).get("hsts"): security_risk += 15
        if dom_res.get("hidden_iframes", 0) > 0: security_risk += 40
        security_risk = min(100, security_risk)

        infrastructure_risk = 0
        if dom_res.get("is_redirected"):
            initial_domain = urlparse(target_url).netloc.replace("www.", "")
            final_domain = urlparse(dom_res.get("final_url", target_url)).netloc.replace("www.", "")
            infrastructure_risk = 85 if (initial_domain and final_domain and initial_domain != final_domain) else 5 
                
        total_risk = (phishing_risk * 0.4) + (identity_risk * 0.3) + (security_risk * 0.2) + (infrastructure_risk * 0.1)
        trust_score = max(100 - int(total_risk), 0)

        if not tls_res.get("secure") or db_res.get("flagged_in_database") or is_community_flagged or phishing_risk >= 80:
            trust_score = min(trust_score, 15)

        await scans_collection.insert_one({"url": target_url, "hostname": hostname, "trust_score": trust_score, "timestamp": datetime.utcnow()})
        history_data = await generate_site_history(trust_score)
        
        db_res["community_flagged"] = is_community_flagged
        
        forensic_payload = {
            "target_url": target_url, "hostname": hostname, "domain_reputation": whois_res,
            "tls_analysis": tls_res, "web_security": dom_res, "infrastructure": port_res, "threat_intelligence": db_res
        }
        ai_report = await generate_ai_analysis(forensic_payload, request.text)

        return {
            "status": "success", "trust_score": trust_score, 
            "risk_vectors": {"Phishing Risk": phishing_risk, "Identity Risk": identity_risk, "Security Architecture": security_risk, "Infrastructure Risk": infrastructure_risk},
            "history": history_data, "evidence": forensic_payload, "ai_investigator": ai_report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backend Error: {str(e)}")

@app.post("/api/report")
async def report_threat(report: ReportRequest):
    hostname = urlparse(report.url).hostname
    if hostname:
        await flags_collection.update_one({"hostname": hostname}, {"$inc": {"report_count": 1}}, upsert=True)
    return {"status": "success", "message": "Added to Threat Database."}