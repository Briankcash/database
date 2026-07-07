from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    count: int

def add_one(state: State):
    return {"count": state["count"] + 1}

builder = StateGraph(State)
builder.add_node("add_one", add_one)
builder.add_edge(START, "add_one")
builder.add_edge("add_one", END)

graph = builder.compile()

result = graph.invoke({"count": 0})
print(result)
