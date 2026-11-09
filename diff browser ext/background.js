// background.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "scanCurrentUrl") {
        // Fetch data from your FastAPI backend, bypassing CORS
        fetch("http://127.0.0.1:8000/api/scan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: request.url })
        })
        .then(response => response.json())
        .then(data => {
            sendResponse({ success: true, data: data });
        })
        .catch(error => {
            sendResponse({ success: false, error: error.message });
        });
        
        return true; // Tells Chrome we will send the response asynchronously
    }
});