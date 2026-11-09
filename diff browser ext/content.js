// content.js

// 1. LISTEN TO YOUR DASHBOARD'S TOGGLE SWITCH
window.addEventListener("message", (event) => {
    // Only accept messages from the window itself
    if (event.source !== window) return;
    
    if (event.data && event.data.type === "TRUSTGUARD_TRACKER_TOGGLE") {
        const isActive = event.data.status === "ON";
        chrome.storage.local.set({ isTrackerActive: isActive }, () => {
            console.log("TRUSTGUARD Tracker globally set to:", isActive ? "ON" : "OFF");
        });
    }
});

// 2. INJECT THE FLOATING WIDGET ON OTHER SITES
chrome.storage.local.get(["isTrackerActive"], (storageData) => {
    const isLocalHost = window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost";
    
    // Do nothing if tracker is OFF or if we are looking at our own dashboard
    if (storageData.isTrackerActive !== true || isLocalHost) {
        return; 
    }

    injectFloatingWidget();
});

function injectFloatingWidget() {
    // Create the container
    const widget = document.createElement("div");
    widget.id = "trustguard-floating-widget";
    
    // Style it like your glassmorphic dashboard
    Object.assign(widget.style, {
        position: "fixed",
        bottom: "20px",
        right: "20px",
        width: "280px",
        backgroundColor: "rgba(15, 23, 42, 0.95)",
        backdropFilter: "blur(10px)",
        border: "1px solid rgba(6, 182, 212, 0.3)",
        borderRadius: "12px",
        padding: "16px",
        color: "#e2e8f0",
        fontFamily: "ui-sans-serif, system-ui, sans-serif",
        boxShadow: "0 10px 25px rgba(0,0,0,0.5), 0 0 15px rgba(6, 182, 212, 0.2)",
        zIndex: "999999",
        transition: "all 0.3s ease",
        display: "flex",
        flexDirection: "column",
        gap: "8px"
    });

    // Initial Loading State
    widget.innerHTML = `
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <strong style="color: #22d3ee; font-size: 14px;">TRUSTGUARD AI</strong>
            <span style="font-size: 12px; color: #94a3b8;" id="tg-status">Scanning...</span>
        </div>
        <div style="height: 4px; width: 100%; background: #334155; border-radius: 2px; overflow: hidden; margin-top: 8px;">
            <div style="height: 100%; width: 50%; background: #22d3ee; animation: tg-slide 1s infinite alternate;"></div>
        </div>
    `;

    // Add a tiny animation style for the loader
    const style = document.createElement('style');
    style.innerHTML = `@keyframes tg-slide { from { transform: translateX(-100%); } to { transform: translateX(200%); } }`;
    document.head.appendChild(style);
    document.body.appendChild(widget);

    // Ask background.js to scan this URL
    chrome.runtime.sendMessage({ action: "scanCurrentUrl", url: window.location.href }, (response) => {
        if (response && response.success) {
            updateWidgetUI(widget, response.data);
        } else {
            widget.innerHTML = `<strong style="color: #ef4444;">Scan Failed</strong><p style="font-size:12px;">Backend offline.</p>`;
            setTimeout(() => widget.remove(), 4000);
        }
    });
}

function updateWidgetUI(widget, data) {
    const score = data.trust_score;
    let color = "#ef4444"; // Red
    let statusText = "CRITICAL THREAT";
    
    if (score > 70) {
        color = "#10b981"; // Green
        statusText = "VERIFIED SAFE";
    } else if (score > 40) {
        color = "#f59e0b"; // Yellow
        statusText = "SUSPICIOUS";
    }

    widget.style.border = `1px solid ${color}`;
    widget.style.boxShadow = `0 10px 25px rgba(0,0,0,0.5), 0 0 15px ${color}40`; // Hex transparency

    widget.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <strong style="color: ${color}; font-size: 12px; letter-spacing: 1px;">${statusText}</strong>
            <button id="tg-close-btn" style="background: none; border: none; color: #94a3b8; cursor: pointer; font-size: 16px;">&times;</button>
        </div>
        <div style="display: flex; align-items: center; gap: 16px;">
            <div style="font-size: 36px; font-weight: 900; color: ${color}; font-family: monospace;">${score}</div>
            <div style="font-size: 11px; color: #cbd5e1; line-height: 1.4;">
                <div>Phishing: <b>${data.risk_vectors['Phishing Risk']}%</b></div>
                <div>Identity: <b>${data.risk_vectors['Identity Risk']}%</b></div>
                <div>Community: <b>${data.evidence.threat_intelligence.community_flagged ? 'Flagged!' : 'Clean'}</b></div>
            </div>
        </div>
    `;

    document.getElementById("tg-close-btn").addEventListener("click", () => {
        widget.remove();
    });
}