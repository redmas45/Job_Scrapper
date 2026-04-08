const API = "http://127.0.0.1:8000/ask";

async function send(){
    let input = document.getElementById("input");
    let chat = document.getElementById("chat-box");
    let cv = document.getElementById("cv").value;

    let q = input.value;

    chat.innerHTML += `<div class="user">${q}</div>`;
    input.value="";

    let res = await fetch(API,{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "x-api-key":"mysecret123"
        },
        body: JSON.stringify({query:q, cv:cv})
    });

    let data = await res.json();

    chat.innerHTML += `<div class="bot">${data.answer}</div>`;
}