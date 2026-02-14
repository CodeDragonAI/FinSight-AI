from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from tools import (
    get_history_text,
    hybrid_search,
    summarize_context,
    extract_sources,
    save_interaction,
)

class ResearchState(TypedDict, total=False):
    query: str
    history_text: str
    context: str
    summary: str
    sources: List[str]

def history_node(state: ResearchState) -> ResearchState:
    state["history_text"] = get_history_text()
    return state

def hybrid_search_node(state: ResearchState) -> ResearchState:
    query = state["query"]
    context = hybrid_search(query)
    state["context"] = context
    return state 

def citation_node(state: ResearchState) -> ResearchState:
    sources = extract_sources(state["context"])
    state["sources"] = sources
    return state

def summarizer_node(state: ResearchState) -> ResearchState:
    summary = summarize_context(
        context=state["context"],
        query=state["query"],
        history=state["history_text"],
        urls = state.get("sources"),
    )
    state["summary"] = summary
    return state

def memory_node(state: ResearchState) -> ResearchState:
    save_interaction(state["query"], state["summary"])
    return state


graph = StateGraph(ResearchState)

graph.add_node("history", history_node)
graph.add_node("search", hybrid_search_node)
graph.add_node("summarize", summarizer_node)
graph.add_node("cite", citation_node)
graph.add_node("memory", memory_node)

graph.set_entry_point("history")
graph.add_edge("history", "search")
graph.add_edge("search", "cite")
graph.add_edge("cite", "summarize")
graph.add_edge("summarize", "memory")
graph.add_edge("memory", END)

workflow = graph.compile()


# while True:
#     user_input = input("Quiz: ")
    
#     if user_input.lower() in ["exit", "quit"]:
#         print("Goodbye!")
#         break
    
#     state = {"query": user_input}
    
#     result = workflow.invoke(state)
    
#     answer = result["summary"]
    
#     print("Bot:", answer)
    
