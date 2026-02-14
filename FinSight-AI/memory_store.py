chat_history: list[dict] = []

def get_recent_history(n: int = 10):
    return chat_history[-n:]

def add_to_history(query: str, summary: str):
    chat_history.append({"query": query, "summary": summary})