# Finance Anomaly Detector

A finance anomaly detection system that combines traditional machine learning with an agentic AI pipeline. Isolation Forest flags unusual transactions, then a multi agent system built with LangGraph investigates each flagged transaction and writes a plain English explanation, running entirely on a local LLM through Ollama.

## What it does

Most anomaly detectors stop at a flag, this transaction is unusual, no further detail. This project goes a step further. Once a transaction is flagged, three agents work together to investigate it.

- **Pattern Agent** compares the transaction to the customer's typical spending behavior
- **Rule Checker Agent** validates the transaction against fixed risk thresholds
- **Explainer Agent** combines both findings into a short, human readable explanation

The result, instead of just "anomaly detected", you get a reason.

## Project structure

```
finance-anomaly-detector/
    data/                  generated and processed datasets
    src/
        generate_data.py     synthetic transaction data using Faker
        inject_mess.py        injects duplicates, nulls, and outliers
        clean_data.py          cleaning pipeline and feature engineering
        detect_anomalies.py    Isolation Forest anomaly detection
        agent_graph.py          LangGraph multi agent investigation pipeline
    dashboard/
        app.py                  Streamlit app for live agent investigation
    requirements.txt
```

## Pipeline

1. **Data generation** — 2,000 synthetic bank transactions generated with Faker, covering customer ID, merchant, category, amount, payment mode, and date
2. **Mess injection** — duplicates, missing merchant and category values, and extreme amount outliers added to simulate real world messy data
3. **Cleaning** — duplicates removed by transaction ID, nulls filled, and features engineered including month, day of week, and a 7 day rolling average spend per customer
4. **Anomaly detection** — Isolation Forest flags roughly 5% of transactions as anomalous based on amount, rolling average, and time based features
5. **Agent investigation** — every flagged transaction is run through a LangGraph pipeline where three agents investigate and explain the anomaly
6. **Visualization** — a Power BI report for overall analytics, and a Streamlit app for live, interactive agent investigation

## Tech stack

Python, pandas, scikit-learn, Faker, LangGraph, LangChain, Ollama (Phi-3), Streamlit, Power BI

## Running it locally

Install dependencies

```
pip install -r requirements.txt
```

Pull the local model through Ollama

```
ollama pull phi3
```

Run the pipeline in order

```
python src/generate_data.py
python src/inject_mess.py
python src/clean_data.py
python src/detect_anomalies.py
python src/agent_graph.py
```

Launch the interactive demo

```
streamlit run dashboard/app.py
```

Enter a transaction amount, customer's rolling average, and category, then watch the agents investigate it in real time.

## Notes

The local LLM (Phi-3 via Ollama) runs entirely offline, no API key or cost involved. Response quality and speed depend on local hardware. Occasional minor inconsistencies in agent wording are a known characteristic of small local models compared to larger hosted ones.
