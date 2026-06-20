from typing import TypedDict
from langgraph.graph import StateGraph, END

class State(TypedDict):
    message: str

def greet_node(state):
    print("Current State:", state)
    return {"message": "Hello from the graph!"}

graph_builder = StateGraph(State)
graph_builder.add_node("greet", greet_node)
graph_builder.set_entry_point("greet")
graph_builder.set_finish_point("greet")
graph = graph_builder.compile()

result = graph.invoke({"message": ""})
print("Final Result:", result)