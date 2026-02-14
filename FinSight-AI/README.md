# FinSight AI – Agentic Financial Research Assistant

An industry-style **agentic financial AI system** using:

* LangGraph (multi-node financial workflow)
* Hybrid RAG (Chroma + Web + Live APIs)
* LLM-based Intent Routing
* Chat history memory
* FastAPI backend
* Real-time financial data integration

---

## Features

* Hybrid retrieval:

  * Local Chroma Vector DB
  * DuckDuckGo web search
  * FRED macroeconomic data
  * Yahoo Finance market data
  * CryptoCompare crypto news
* Intelligent intent routing:

  * `macro` → FRED API
  * `market` → Yahoo Finance
  * `crypto` → CryptoCompare
  * `general` → RAG + Web
* LangGraph workflow:

  * history → intent → hybrid search → cite → summarize → memory
* Structured 7-bullet financial research output
* Memory-aware contextual answers
* Production-ready `/query`, `/ingest`, `/health` APIs

---

## Architecture Flow

User Query
→ Intent Detection (LLM Router)
→ Hybrid Search
  • Chroma Vector DB
  • Web Search
  • Live Financial APIs
→ Citation Extraction
→ LLM Summarization
→ Memory Storage
→ Structured Response

---

## Tech Stack

* Python
* LangChain
* LangGraph
* FastAPI
* Chroma Vector DB
* Ollama Embeddings
* OpenRouter (GPT-4o-mini)
* yfinance
* FRED API
* CryptoCompare API
* Pydantic
* dotenv

---

## Project Structure

```
FinSight-AI/
│
├── app.py
├── graph.py
├── tools.py
├── rag_store.py
├── memory_store.py
├── test.py
│
├── api_engines/
│   ├── crypto_engine.py
│   ├── fred_engine.py
│   ├── market_engine.py
│   └── intent_detection.py
```

---

## Run

```bash
pip install -r requirements.txt

# create .env file
OPENAI_API_KEY=your_key_here
FRED_API_KEY=your_key_here
ADMIN_SECRET=your_secret
CHROMA_DIR=./chroma_db

uvicorn app:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

---

## API Endpoints

### POST `/query`

Returns structured financial research summary.

### POST `/ingest`

Admin-only document ingestion into vector database.

### GET `/health`

Service health check.

---

## What This Project Demonstrates

* Agentic AI system design
* Hybrid RAG implementation
* Financial API orchestration
* LLM-based tool routing
* Vector database engineering
* Memory-aware AI agents
* Production-ready AI backend architecture

---

## Future Improvements

* Persistent memory (Redis / PostgreSQL)
* Streaming responses
* Frontend dashboard (Next.js)
* Multi-agent collaboration
* Risk analytics engine
* Portfolio optimization module

