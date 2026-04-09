# 🚀 AI Job Agent — Personalized RAG-Based Job Recommendation System

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/API-FastAPI-green)
![FAISS](https://img.shields.io/badge/VectorDB-FAISS-orange)
![Grok](https://img.shields.io/badge/LLM-Grok%20API-red)
![Railway](https://img.shields.io/badge/Hosted-Railway-purple)

---

## 🧠 Overview

AI Job Agent is a personalized job recommendation system powered by RAG (Retrieval-Augmented Generation).

It scrapes jobs, builds embeddings, and uses an LLM to generate job recommendations tailored to your CV.

---

## 🖥️ Demo UI

![App UI](./ui.png)

---

## 🔥 Key Features

- Multi-source Job Scraping
- Semantic Search using FAISS
- Multi-CV Support
- Smart Deduplication (SQLite)
- Grok LLM Integration
- Chat-based Interface
- Intelligent Query Routing
- Railway Deployment

---

## 🏗️ System Architecture

```
┌─────────────┐
│  Web UI     │
└──────┬──────┘
       │
       ↓
┌──────────────────┐
│  FastAPI Backend │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
    ↓         ↓
┌─────────┐ ┌──────────┐
│  FAISS  │ │  Grok    │
│ Vector  │ │   LLM    │
│ Search  │ │   API    │
└────┬────┘ └──────────┘
     │
     ↓
┌──────────┐
│  SQLite  │
│   Jobs   │
└──────────┘
```

---

## 📁 Project Structure

```
Job_Scrapper/
├── app.py
├── config.py
├── pipeline.py
├── requirements.txt
├── data/
├── embeddings/
├── rag/
├── vector_db/
└── frontend/
```

---

## 🌐 Live Deployment

https://web-production-c0217.up.railway.app

---

## 🚀 Local Setup

```bash
git clone https://github.com/redmas45/Job_Scrapper.git
cd Job_Scrapper
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

```env
PINECONE_API_KEY=your_key
PINECONE_INDEX=jobs-index
GROK_API_KEY=your_key
API_KEY=mysecret123
```

---

## ▶️ Run Locally

```bash
uvicorn app:app --reload
```

Frontend:
```bash
cd frontend
python -m http.server 8080
```

---

## 🌐 Railway Deployment

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Railway deployment"
git push origin main
```

### Step 2: Create Railway Project
1. Go to https://railway.app  
2. Click **New Project**  
3. Select **Deploy from GitHub Repo**  
4. Choose your repository  

### Step 3: Configure Start Command
```bash
uvicorn app:app --host 0.0.0.0 --port $PORT
```

### Step 4: Add Environment Variables
```
PINECONE_API_KEY=pcsk_xxxxx
PINECONE_INDEX=jobs-index
GROK_API_KEY=gsk_xxxxx
API_KEY=mysecret123
```

### Step 5: Deploy
Click **Deploy** and wait 2–3 minutes.

Test:
```
https://web-production-c0217.up.railway.app/health
```

---

## 📡 API

### GET `/health`
```json
{
  "status": "ok"
}
```

---

### POST `/ask`

```json
{
  "query": "Find ML jobs",
  "cv": "1"
}
```

---

## 🔍 Usage Examples

### Ask About Your CV
```javascript
const response = await fetch('https://web-production-c0217.up.railway.app/ask', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-api-key': 'mysecret123'
  },
  body: JSON.stringify({
    query: 'What technologies did I work with?',
    cv: '1'
  })
});
```

### Find Job Recommendations
```javascript
const response = await fetch('https://web-production-c0217.up.railway.app/ask', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'x-api-key': 'mysecret123'
  },
  body: JSON.stringify({
    query: 'Find computer vision engineer jobs',
    cv: '1'
  })
});
```

---

## 🧱 Tech Stack

| Layer | Tech |
|------|------|
| Backend | FastAPI |
| LLM | Grok |
| Vector DB | FAISS / Pinecone |
| DB | SQLite |
| Frontend | HTML/CSS/JS |
| Hosting | Railway |

---

## 👤 Author

Rajiv Kumar  
ML Engineer — Computer Vision & GenAI

---

## ⭐ Support

Give it a ⭐ on GitHub if you like it!
