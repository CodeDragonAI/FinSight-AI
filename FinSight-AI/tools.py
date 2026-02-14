import os
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from rag_store import semantic_search
from memory_store import get_recent_history, add_to_history

from api_engines.fred_engine import get_fred_data
from api_engines.market_engine import get_market_price
from api_engines.crypto_engine import get_crypto_news
from api_engines.intent_detection import llm_router


llm = ChatOpenAI(
    model="gpt-4o-mini",  
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"),  
    base_url="https://openrouter.ai/api/v1"
)

search_tool = DuckDuckGoSearchRun()

def get_history_text() -> str:
    history = get_recent_history()
    if not history:
        return ""
    lines = []
    for h in history:
        lines.append(f"Q: {h['query']}\nA: {h['summary']}")
    return "\n\n".join(lines)

def hybrid_search(query: str) -> str:

    local_text = semantic_search(query, k=2)
    web_text = search_tool.run(query)

    api_data = ""
    routing = llm_router(query)

    intent = routing.get("intent")

    if intent == "macro":
        series_id = routing.get("series_id")
        if series_id:
            api_data = get_fred_data(series_id)

    elif intent == "market":
        symbol = routing.get("symbol")
        if symbol:
            api_data = get_market_price(symbol)

    elif intent == "crypto":
        api_data = get_crypto_news()


    return f"LOCAL:\n{local_text}\n\nWEB:\n{web_text}\n\nLIVE DATA:\n{api_data}" 

def summarize_context(context: str, query: str, history: str, urls:str) -> str:
    prompt = f"""
        You are a helpful research assistant.

        User question:
        {query}

        Recent chat history:
        {history}

        Context from RAG (local + web + live data):
        {context}

        resources (web urls)
        {urls}

        Task:
        - Answer the question in 7 bullet points.
        - Be concise and clear.
        - If unsure, say you are not fully certain.
        - If URLs are provided, include a "Sources:" section at the end with links to the websites.
        - If no URLs are provided, do not include a "Sources:" section.
    """
    return llm.invoke(prompt).content

def extract_sources(context: str) -> list[str]:
    tokens = context.split()
    urls = [t for t in tokens if t.startswith("http")]
    return urls[:3]

def save_interaction(query: str, summary: str):
    add_to_history(query, summary)

