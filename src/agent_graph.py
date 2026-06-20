from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
import pandas as pd

llm = ChatOllama(model="phi3")

class State(TypedDict):
    customer_id: str
    amount: float
    rolling_avg_7d: float
    category: str
    pattern_finding: str
    rule_finding: str
    final_explanation: str

def pattern_node(state):
    prompt = f"""A customer typically spends around ${state['rolling_avg_7d']} on average.
This transaction was ${state['amount']} in the category {state['category']}.
In one short sentence, describe how unusual this transaction is compared to their typical spending."""
    
    response = llm.invoke(prompt)
    return {"pattern_finding": response.content}


def rule_node(state):
    ratio = state["amount"] / state["rolling_avg_7d"]
    
    if ratio > 5:
        finding = f"Transaction is {ratio:.1f}x the rolling average, exceeds high risk threshold of 5x."
    elif ratio > 2:
        finding = f"Transaction is {ratio:.1f}x the rolling average, exceeds moderate risk threshold of 2x."
    else:
        finding = f"Transaction is {ratio:.1f}x the rolling average, within normal range."
    
    return {"rule_finding": finding}


def explainer_node(state):
    prompt = f"""Based on these two findings, write a single short professional explanation for why this transaction was flagged as anomalous.

Pattern finding: {state['pattern_finding']}
Rule finding: {state['rule_finding']}

Write only the final explanation, 1-2 sentences, no preamble."""
    
    response = llm.invoke(prompt)
    return {"final_explanation": response.content}

graph_builder = StateGraph(State)
graph_builder.add_node("pattern", pattern_node)
graph_builder.add_node("rule", rule_node)
graph_builder.add_node("explainer", explainer_node)

graph_builder.set_entry_point("pattern")
graph_builder.add_edge("pattern", "rule")
graph_builder.add_edge("rule", "explainer")
graph_builder.add_edge("explainer", END)

graph = graph_builder.compile()

df = pd.read_csv("data/transactions_anomalies.csv")
df = df[df["anomaly_flag"] == 1].reset_index(drop=True)

explanations = []

for i, row in df.iterrows():
    state = {
        "customer_id": row["customer_id"],
        "amount": row["amount"],
        "rolling_avg_7d": row["rolling_avg_7d"],
        "category": row["category"],
        "pattern_finding": "",
        "rule_finding": "",
        "final_explanation": ""
    }
    print(f"Processing row {i}")
    result = graph.invoke(state)
    explanations.append(result["final_explanation"])

df["final_explanation"] = explanations
df.to_csv("data/transactions_with_explanations.csv", index=False)
print("Done, saved to transactions_with_explanations.csv")