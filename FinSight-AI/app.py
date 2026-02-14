import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Header, HTTPException
from graph import workflow
from rag_store import add_document

app = FastAPI(title="Agentic AI Research Assistant")

class QueryRequest(BaseModel):
    query: str

class IngestRequest(BaseModel):
    text: str

@app.post("/query")
def query_endpoint(body: QueryRequest):
    state = {"query": body.query}
    result = workflow.invoke(state)
    return {
        "query": body.query,
        "summary": result.get("summary", ""),
    }


ADMIN_SECRET = os.getenv("ADMIN_SECRET")

@app.post("/ingest")
def ingest_endpoint(body: IngestRequest, x_admin_key: str = Header(None)):

    if x_admin_key != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Not authorized")

    add_document(body.text)
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"status": "running"}