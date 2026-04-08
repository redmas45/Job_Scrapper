const API = "https://job-scrapper-0x72.onrender.com";

async function send(){
    let input = document.getElementById("input");
    let chat = document.getElementById("chat-box");
    let cv = document.getElementById("cv").value;

    let q = input.value;

    if (!q.trim()) return;

    chat.innerHTML += `<div class="user">${q}</div>`;
    input.value="";

    // Show loading indicator
    chat.innerHTML += `<div class="bot">⏳ Loading...</div>`;

    try {
        let res = await fetch(API + "/ask", {
            method:"POST",
            headers:{
                "Content-Type":"application/json",
                "x-api-key":"mysecret123"
            },
            body: JSON.stringify({query:q, cv:cv})
        });

        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }

        let data = await res.json();

        // Remove loading indicator and show answer
        let botMessages = document.querySelectorAll(".bot");
        botMessages[botMessages.length - 1].textContent = data.answer;
    } catch (error) {
        console.error("Error:", error);
        chat.innerHTML += `<div class="bot">❌ Error: ${error.message}</div>`;
    }

    chat.scrollTop = chat.scrollHeight;
}