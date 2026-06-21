import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from agent_graph import graph
import re

st.title("Finance Anomaly Investigator")
st.write("Enter a transaction below to see how the AI agents investigate it in real time.")

customer_id = st.text_input("Customer ID", value="CUST001")
amount = st.number_input("Transaction Amount ($)", value=100.0)
rolling_avg = st.number_input("Customer's Rolling 7-Day Average ($)", value=500.0)
category = st.selectbox("Category", ["groceries", "travel", "dining", "shopping", "utilities", "entertainment"])

if st.button("Investigate Transaction"):
    state = {
        "customer_id": customer_id,
        "amount": amount,
        "rolling_avg_7d": rolling_avg,
        "category": category,
        "pattern_finding": "",
        "rule_finding": "",
        "final_explanation": ""
    }
    
    with st.spinner("Pattern Agent investigating..."):
        result = graph.invoke(state)
    
    def clean(text):
        return re.sub(r'[`´‘’]', '', text)
    
    st.subheader("Pattern Agent")
    st.text(clean(result["pattern_finding"]))

    st.subheader("Rule Checker Agent")
    st.text(clean(result["rule_finding"]))

    st.subheader("Final Explanation")
    st.text(clean(result["final_explanation"]))