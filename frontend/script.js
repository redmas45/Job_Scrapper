// Railway deployment URL
const API = "web-production-95aec.up.railway.app";
const TIMEOUT = 30000; // 30 seconds

// Check if backend is alive
async function checkBackendHealth() {
    try {
        const res = await fetch(API + "/health", {
            method: "GET",
            timeout: 5000
        });
        return res.ok;
    } catch (e) {
        return false;
    }
}

async function send(){
    let input = document.getElementById("input");
    let chat = document.getElementById("chat-box");
    let cv = document.getElementById("cv").value;

    let q = input.value;

    if (!q.trim()) return;

    chat.innerHTML += `<div class="user">${q}</div>`;
    input.value="";

    // Show loading indicator
    let loadingId = Date.now();
    chat.innerHTML += `<div class="bot" id="loading-${loadingId}">⏳ Contacting server...</div>`;
    chat.scrollTop = chat.scrollHeight;

    try {
        // Timeout mechanism
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), TIMEOUT);

        let res = await fetch(API + "/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "x-api-key": "mysecret123"
            },
            body: JSON.stringify({query: q, cv: cv}),
            signal: controller.signal
        });

        clearTimeout(timeout);

        if (!res.ok) {
            throw new Error(`Server error: ${res.status} - ${res.statusText}`);
        }

        let data = await res.json();

        // Replace loading with actual answer
        let loadingEl = document.getElementById(`loading-${loadingId}`);
        if (loadingEl) {
            loadingEl.textContent = data.answer || "No response received";
        }
    } catch (error) {
        console.error("Error details:", error);
        
        let errorMsg = "❌ Error: ";
        if (error.name === "AbortError") {
            errorMsg += "Request timeout (server not responding)";
        } else if (error.message.includes("Failed to fetch")) {
            errorMsg += "Cannot reach server. Check if Render is running.";
        } else {
            errorMsg += error.message;
        }

        let loadingEl = document.getElementById(`loading-${loadingId}`);
        if (loadingEl) {
            loadingEl.textContent = errorMsg;
        }
    }

    chat.scrollTop = chat.scrollHeight;
}

// Check backend on page load
document.addEventListener("DOMContentLoaded", async () => {
    const isHealthy = await checkBackendHealth();
    if (!isHealthy) {
        const chat = document.getElementById("chat-box");
        chat.innerHTML = `<div class="bot">⚠️ Warning: Backend server may not be responding. Make sure Render deployment is active.</div>`;
    }
});