from langchain_ollama import ChatOllama

llm = ChatOllama(model="phi3")
response = llm.invoke("Explain in one sentence why a $5000 transaction might be flagged as unusual.")
print(response.content)