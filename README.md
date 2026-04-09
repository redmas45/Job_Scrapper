# 🚀 AI Job Agent — Personalized RAG-Based Job Recommendation System

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/API-FastAPI-green)
![FAISS](https://img.shields.io/badge/VectorDB-FAISS-orange)
![Grok](https://img.shields.io/badge/LLM-Grok%20API-red)
![Render](https://img.shields.io/badge/Hosted-Render-blueviolet)

---

## 🧠 Overview

**AI Job Agent** is a fully automated, personalized job recommendation system powered by **Retrieval-Augmented Generation (RAG)**.

It scrapes jobs from multiple platforms, stores them in SQLite, converts them into semantic embeddings, and uses an LLM (Grok API) to generate personalized recommendations matching your CV.

> ⚡ Think of it as your own **private AI recruiter** — ask about jobs or your CV, get instant recommendations!

---

## 🔥 Key Features

- 🕵️ **Multi-source Job Scraping** — Indeed, LinkedIn, Google, ZipRecruiter for ML/AI roles
- 🧠 **Semantic Search** — FAISS for fast vector-based job matching
- 📄 **Multi-CV Support** — GenAI & Computer Vision profile variants
- ⚡ **Smart Deduplication** — SQLite DB with auto-cleanup (72hr TTL)
- 🤖 **Grok LLM Integration** — Cloud-based, no local setup needed
- 💬 **Interactive Chat Mode** — Ask about jobs or your CV qualifications
- 🎯 **Query Routing** — Intelligent switching between CV and job context
- 🌐 **Web Interface** — Beautiful chat UI with real-time responses
- 🚀 **Cloud Deployment** — One-click deployment on Render

---

## 🏗️ System Architecture

```
┌─────────────┐
│ Web Chat UI │
└──────┬──────┘
       │
       ↓
┌──────────────────┐
│  FastAPI Backend │
└────────┬─────────┘
         │
    ┌────┴────┐
    │          │
    ↓          ↓
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
├── app.py                 # FastAPI server
├── config.py              # Configuration & secrets
├── pipeline.py            # CLI tool for scraping/embedding
├── requirements.txt       # Python dependencies
├── Procfile               # Render deployment config
│
├── data/
│   ├── db.py              # SQLite database operations
│   ├── save_jobs.py       # Job scraping logic (JobSpy)
│   ├── jobs.db            # Local job database
│   ├── Rajiv_Kumar_G.pdf  # CV sample 1 (GenAI)
│   └── Rajiv_Kumar_M.pdf  # CV sample 2 (Computer Vision)
│
├── embeddings/
│   ├── embed_jobs.py      # Embedding generation
│   ├── search_jobs.py     # FAISS search operations
│   ├── faiss.index        # Pre-built FAISS index
│   └── metadata.json      # Job metadata
│
├── rag/
│   ├── generate.py        # LLM response generation (Grok)
│   └── read_cv.py         # PDF CV parsing
│
├── vector_db/
│   ├── search.py          # Unified search interface
│   └── pinecone_client.py # Pinecone integration (optional)
│
└── frontend/
    ├── index.html         # Web UI
    ├── script.js          # Frontend logic
    └── style.css          # Styling
```

---

## 🚀 Quick Start

### Local Setup

#### Prerequisites
- Python 3.11+
- pip

#### Step 1: Clone & Setup

```bash
git clone https://github.com/redmas45/Job_Scrapper.git
cd Job_Scrapper
python -m venv venv
venv\Scripts\activate  # Windows
```

#### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Configure Environment

Create `.env` file (copy from `.env.example`):

```env
PINECONE_API_KEY=your_key
PINECONE_INDEX=jobs-index
GROK_API_KEY=your_key
API_KEY=mysecret123
```

#### Step 4: Run Locally

**Terminal 1 - Backend:**
```bash
uvicorn app:app --reload
```
Server runs on: `http://127.0.0.1:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend
python -m http.server 8080
```
Open browser: `http://localhost:8080`

---

## 🌐 Deploy on Render

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for Render"
git push origin main
```

### Step 2: Create Render Service

1. Go to [Render.com](https://render.com)
2. Click **"New Web Service"**
3. Connect your GitHub repo
4. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port 8000`

### Step 3: Set Environment Variables

In Render Dashboard → Settings → Environment:

```
PINECONE_API_KEY=pcsk_xxxxx
PINECONE_INDEX=jobs-index
GROK_API_KEY=gsk_xxxxx
API_KEY=mysecret123
```

### Step 4: Deploy

Click **"Create Web Service"** and wait 3-5 minutes.

Test: `https://your-app-name.onrender.com/health`

---

## 📡 API Documentation

### Endpoints

#### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "Backend is running"
}
```

#### POST `/ask`
Query the job recommendation system.

**Headers:**
```
x-api-key: mysecret123
Content-Type: application/json
```

**Request Body:**
```json
{
  "query": "What are good ML jobs for me?",
  "cv": "1"
}
```

**Response:**
```json
{
  "answer": "Based on your CV, I recommend these positions..."
}
```

**Query Types:**
- CV Questions: "What's my experience?", "List my skills"
- Job Questions: "Find ML engineer jobs", "What jobs match my CV?"

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `PINECONE_API_KEY` | Pinecone API key | Yes (optional if using FAISS) |
| `PINECONE_INDEX` | Pinecone index name | Yes (if using Pinecone) |
| `GROK_API_KEY` | X.AI Grok API key | Yes |
| `API_KEY` | FastAPI security key | Yes |

### Supported CV Formats
- `cv: "1"` → Rajiv_Kumar_G.pdf (GenAI profile)
- `cv: "2"` → Rajiv_Kumar_M.pdf (Computer Vision profile)

---

## 🔍 Usage Examples

### Ask About Your CV
```javascript
const response = await fetch('https://job-scrapper.onrender.com/ask', {
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
const response = await fetch('https://job-scrapper.onrender.com/ask', {
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

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| **Module not found** | Run `pip install -r requirements.txt` |
| **API key error** | Check `.env` file has correct keys |
| **No job results** | Ensure FAISS index exists in `embeddings/` |
| **Timeout errors** | Increase timeout in `script.js` (currently 30s) |
| **Render deployment fails** | Check Build Logs in Render dashboard |

---

## 🔐 Security

⚠️ **Never commit** `.env` file to GitHub. Use:
- Local `.env` for development
- Render Environment Variables for production

### API Security
- All requests require `x-api-key` header
- Change default key in production
- Use environment variables for all secrets

---

## 🚀 Future Improvements

- [ ] Support for more CV formats (DOCX, TXT)
- [ ] Batch job scraping scheduling
- [ ] Advanced filtering (salary, location, experience)
- [ ] Job notification system
- [ ] Analytics dashboard
- [ ] Multi-language support

---

## 📝 License

[MIT License](LICENSE)

---

## 👤 Author

**Rajiv Kumar**

---

## ❓ Questions?

For issues or questions, open a GitHub issue or contact the maintainer.

**Happy job hunting!** 🎉

```text
1 → Full pipeline (scrape + embed + search)
2 → Fast mode (use existing DB + FAISS)
3 → Only scrape
4 → Only embed
```

---

## 📄 CV Selection

```text
1 → GenAI CV
2 → Computer Vision CV
```

---

## 💬 Chat Mode

```text
🔍 Query: best jobs for me
🔍 Query: remote CV jobs
🔍 Query: what sensors I worked on
🔍 Query: exit
```

---

## 🧠 How It Works

### 🔹 1. Scraping

* Uses JobSpy to fetch jobs
* Filters duplicates
* Stores in SQLite

---

### 🔹 2. Database Layer

* Deduplication using:

```text
title + company + location
```

* Automatic cleanup:

```text
Jobs older than 72 hours removed
```

---

### 🔹 3. Embedding

* Model: `all-MiniLM-L6-v2`
* Cosine similarity via FAISS
* Incremental updates (only new jobs embedded)

---

### 🔹 4. RAG Pipeline

* Query routing:

  * CV-only questions → CV context
  * Job queries → CV + FAISS results

---

### 🔹 5. LLM (Ollama) (local)

* Default: `phi`
* Optional:

  * `llama3`
  * `gemma`

---

## 🎯 Example Outputs

### ✅ CV-based question

```text
Query: What sensors I worked on?

Answer:
You have worked with RGB, UV, and hyperspectral sensors.
```

---

### ✅ Job recommendation

```text
Query: Top jobs for me

Answer:
Based on your computer vision experience:
1. Computer Vision Engineer
2. AI Vision Engineer
...
```

---

## ⚡ Performance Optimizations

* ✅ Incremental embeddings
* ✅ Early stopping in scraping
* ✅ Batch encoding
* ✅ Cosine similarity (normalized vectors)
* ✅ SQLite indexing

---

## 🔐 Security Notes

- Never commit `.env` to GitHub — use `.gitignore`
- Change `API_KEY` from the default before deploying publicly
- Store all secrets in Railway/Render environment variables

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Uvicorn |
| LLM | Groq — LLaMA 3.3 70B Versatile |
| Embeddings | sentence-transformers/all-distilroberta-v1 |
| Vector DB | FAISS (local) / Pinecone (optional) |
| Job Scraping | JobSpy |
| Database | SQLite |
| Frontend | Vanilla HTML/CSS/JS |
| Hosting | Railway |


## 👤 Author

**Rajiv Kumar** — ML Engineer with focus on Computer Vision and Generative AI

---

## ⭐ If this helped you

Give it a star on GitHub — it helps others find the project!

