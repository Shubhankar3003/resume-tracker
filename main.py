import uuid
import io
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from pypdf import PdfReader

from db import collection
from models import ApplicationStatus, StatusUpdateRequest

app = FastAPI(title="Resume Tracker")

def parse_file(file_bytes: bytes, filename: str) -> str:
    # Extracts text from PDF documents using pypdf
    if filename.lower().endswith(".pdf"):
        reader = PdfReader(io.BytesIO(file_bytes))
        return "\n".join([page.extract_text() or "" for page in reader.pages]).strip()
    # Decodes plain text files
    elif filename.lower().endswith((".txt", ".md")):
        return file_bytes.decode("utf-8", errors="ignore").strip()
    raise HTTPException(status_code=400, detail="Invalid file type. Upload PDF or TXT.")

@app.post("/api/resumes/upload")
async def upload_resume(
    file: UploadFile = File(...),
    name: str = Form(...),
    email: str = Form(...),
    designation: str = Form(...),
    experience_years: float = Form(...),
    skills: str = Form(...),
    location: str = Form(...),
    education: str = Form(...),
    status: ApplicationStatus = Form(ApplicationStatus.APPLIED)
):
    contents = await file.read()
    raw_text = parse_file(contents, file.filename)
    if not raw_text:
        raw_text = f"{name} {designation} with skills: {skills}"

    candidate_id = str(uuid.uuid4())

    # Structures combined text representation for semantic vectorization
    doc_text = (
        f"Name: {name}\n"
        f"Role: {designation}\n"
        f"Skills: {skills}\n"
        f"Experience: {experience_years} years\n"
        f"Location: {location}\n"
        f"Education: {education}\n\n"
        f"{raw_text}"
    )

    # Metadata dictionary for structured filtering
    meta = {
        "candidate_id": candidate_id,
        "name": name,
        "email": email,
        "designation": designation.strip().lower(),
        "experience_years": float(experience_years),
        "skills": skills.strip().lower(),
        "location": location.strip().lower(),
        "education": education.strip().lower(),
        "status": status.value,
        "filename": file.filename
    }

    # Stores text embedding and associated metadata in collection
    collection.add(
        ids=[candidate_id],
        documents=[doc_text],
        metadatas=[meta]
    )

    return {"candidate_id": candidate_id, "status": status.value}

@app.get("/api/candidates/search")
async def search_candidates(
    query: str = Query(...),
    min_experience: Optional[float] = None,
    location: Optional[str] = None,
    status: Optional[ApplicationStatus] = None,
    top_k: int = 5
):
    # Constructs structured metadata filters for ChromaDB
    where_clauses = []
    if min_experience is not None:
        where_clauses.append({"experience_years": {"$gte": float(min_experience)}})
    if status is not None:
        where_clauses.append({"status": {"$eq": status.value}})

    where_filter = None
    if len(where_clauses) == 1:
        where_filter = where_clauses[0]
    elif len(where_clauses) > 1:
        where_filter = {"$and": where_clauses}

    # Executes semantic vector search
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where=where_filter
    )

    candidates = []
    if results and results["ids"] and len(results["ids"][0]) > 0:
        for idx in range(len(results["ids"][0])):
            meta = results["metadatas"][0][idx]
            dist = results["distances"][0][idx]

            # Converts cosine distance to normalized similarity percentage
            relevance = max(0.0, min(1.0, 1.0 - dist))

            # Applies substring matching for flexible city filtering
            if location and location.lower() not in meta["location"]:
                continue

            candidates.append({
                **meta,
                "relevance_score": f"{round(relevance * 100, 2)}%"
            })

    return {"query": query, "total": len(candidates), "candidates": candidates}

@app.post("/api/candidates/match-jd")
async def match_jd(job_description: str = Form(...), top_k: int = 5):
    # Matches complete job description text against candidate embeddings
    results = collection.query(query_texts=[job_description], n_results=top_k)
    ranked = []
    if results and results["ids"] and len(results["ids"][0]) > 0:
        for idx in range(len(results["ids"][0])):
            meta = results["metadatas"][0][idx]
            dist = results["distances"][0][idx]
            ranked.append({
                "rank": idx + 1,
                **meta,
                "match_score": f"{round((1.0 - dist) * 100, 2)}%"
            })
    return {"ranked": ranked}

@app.patch("/api/candidates/{candidate_id}/status")
async def update_status(candidate_id: str, payload: StatusUpdateRequest):
    existing = collection.get(ids=[candidate_id])
    if not existing or not existing["ids"]:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Updates recruitment status in metadata without re-computing vectors
    meta = existing["metadatas"][0]
    meta["status"] = payload.status.value
    collection.update(ids=[candidate_id], metadatas=[meta])
    return {"message": f"Updated to {payload.status.value}", "candidate_id": candidate_id}

@app.get("/api/candidates")
async def get_candidates():
    # Returns all indexed candidates in storage
    records = collection.get()
    items = [records["metadatas"][i] for i in range(len(records["ids"]))] if records and records["ids"] else []
    return {"total": len(items), "candidates": items}