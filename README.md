# Resume Tracker

A candidate tracking and semantic resume search service built with FastAPI, ChromaDB, and sentence embeddings.

---

## Overview

Vector Storage:
Local persistent ChromaDB instance configured with cosine distance indexing (`hnsw:space: cosine`).

Embedding Pipeline:
Open-source `sentence-transformers/all-MiniLM-L6-v2` generating 384-dimensional dense semantic vectors.

Hybrid Candidate Search:
Combines strict metadata filtering (years of experience, target city, application status) with semantic vector similarity ranking.

ATS Lifecycle Management:
Tracks candidate stages across `Applied`, `Screening`, `Shortlisted`, `Interview`, `Selected`, and `Rejected`.

---

## Project Structure

resume_tracker/
├── db.py           # ChromaDB client & SentenceTransformer initialization
├── models.py       # Pydantic schemas & ApplicationStatus enum
├── main.py         # FastAPI endpoints & file parsing logic
├── seed_data.py    # Sample candidate ingestion script
└── requirements.txt# Project dependencies

## Quick Start

# 1. Create the virtual environment
python3 -m venv venv

# 2. Activate the virtual environment

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# 3. Install required dependencies
pip install -r requirements.txt

# 4. Start the API Server
uvicorn main:app --reload --port 8000

# 5. Seed Sample Candidate Data
source venv/bin/activate
python seed_data.py

# 6. Interactive API
Open your browser and navigate to:

http://127.0.0.1:8000/docs

