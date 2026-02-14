import os
from dotenv import load_dotenv

load_dotenv() 

from langchain_openai import ChatOpenAI
import json

router_llm = ChatOpenAI(
    model="gpt-4o-mini",  
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"),  
    base_url="https://openrouter.ai/api/v1"
)

def llm_router(query: str) -> dict:
    prompt = f"""
You are a financial intent detection engine.

Classify the query into:
- macro
- market
- crypto
- general

If macro: return the correct FRED series id (e.g. CPIAUCSL, UNRATE, GDP, FEDFUNDS, M2SL).
If market: return the Yahoo Finance symbol (e.g. ^GSPC, ^NSEI, GC=F).
If crypto: return coin name if mentioned.

Return JSON like:
{{
    "intent": "",
    "series_id": "",
    "symbol": "",
    "coin": ""
}}

Query: {query}
"""

    response = router_llm.invoke(prompt).content

    try:
        return json.loads(response)
    except:
        return {"intent": "general"}


