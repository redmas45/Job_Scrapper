# 🚀 AI Job Agent — Personalized RAG-Based Job Recommendation System

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FAISS](https://img.shields.io/badge/VectorDB-FAISS-orange)
![Ollama](https://img.shields.io/badge/LLM-Ollama-green)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## 🧠 Overview

**AI Job Agent** is a fully automated, personalized job recommendation system powered by **Retrieval-Augmented Generation (RAG)**.

It scrapes jobs from multiple platforms, stores them in a local database, converts them into embeddings, and uses a local LLM to recommend the most relevant jobs based on **your CV**.

> ⚡ Think of it as your own **private LinkedIn AI recruiter — running locally**

---

## 🔥 Key Features

* 🕵️ **Multi-source Job Scraping** (Indeed, LinkedIn, Google, ZipRecruiter)
* 🧠 **Semantic Search with FAISS**
* 📄 **Multi-CV Personalization (GenAI / Computer Vision profiles)**
* ⚡ **Incremental Embeddings (no recomputation)**
* 🗄️ **SQLite Database with Deduplication + 72hr TTL**
* 🤖 **Local LLM (Ollama - Phi / Llama / Gemma)**
* 💬 **Interactive Chat Mode (multi-query like ChatGPT)**
* 🎯 **Query Routing (CV vs Job Queries)**
* 🚀 **Pipeline Modes (Full / Fast / Partial Execution)**

---

## 🏗️ System Architecture

```text
            ┌────────────────────┐
            │   Job Scraping     │
            │   (JobSpy)         │
            └─────────┬──────────┘
                      ↓
            ┌────────────────────┐
            │   SQLite DB        │
            │ Dedup + TTL (72h)  │
            └─────────┬──────────┘
                      ↓
            ┌────────────────────┐
            │   Embeddings       │
            │ MiniLM (HF Model) │
            └─────────┬──────────┘
                      ↓
            ┌────────────────────┐
            │   FAISS Index      │
            │ (Vector Search)    │
            └─────────┬──────────┘
                      ↓
            ┌────────────────────┐
            │   RAG Pipeline     │
            │ CV + Jobs Context  │
            └─────────┬──────────┘
                      ↓
            ┌────────────────────┐
            │   LLM (Ollama)     │
            │ Phi / Llama / Gemma│
            └────────────────────┘
```

---

## 📁 Project Structure

```text
Job_Scrapper/
│
├── data/
│   ├── db.py              # SQLite DB logic
│   ├── save_jobs.py       # Scraping + storage
│   ├── jobs.db            # Local database
│   ├── cv1.pdf            # GenAI CV
│   └── cv2.pdf            # Computer Vision CV
│
├── embeddings/
│   ├── embed_jobs.py      # Incremental embeddings
│   ├── search_jobs.py     # FAISS search
│   ├── faiss.index
│   └── metadata.json
│
├── rag/
│   ├── generate.py        # LLM response generation
│   └── read_cv.py         # CV parsing
│
├── pipeline.py            # Main entry point
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/ai-job-agent.git
cd ai-job-agent
```

---

### 2️⃣ Create Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Install Ollama

Download & install:

👉 Ollama

Then run:

```bash
ollama run phi
```

---

## 🚀 Usage

Run the pipeline:

```bash
python pipeline.py
```

---

## 🎮 Modes

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

### 🔹 5. LLM (Ollama)

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

## 🚀 Future Improvements

* 📊 Job scoring system (CV match %)
* 📧 Email automation (daily alerts)
* 🌐 FastAPI backend
* ☁️ Pinecone integration
* 🐳 Docker deployment
* 🖥️ UI (Streamlit / React)

---

## 🧠 Tech Stack

| Component  | Technology           |
| ---------- | -------------------- |
| Scraping   | JobSpy               |
| DB         | SQLite               |
| Embeddings | SentenceTransformers |
| Vector DB  | FAISS                |
| LLM        | Ollama               |
| Language   | Python               |

---

## ⚠️ Limitations

* Scraping APIs are unstable
* FAISS is local (not scalable)
* CV parsing depends on PDF quality

---

## 🤝 Contributing

Pull requests are welcome!

---

## 📜 License

MIT License

---

## 💡 Author

**Rajiv Kumar**

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!

---

# 🔥 Final Thought

```text
This is not just a project.
This is your personal AI job agent.
```
