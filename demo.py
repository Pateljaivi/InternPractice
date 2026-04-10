from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# Initialize model
llm = ChatOllama(
    model="llama3.2:latest",  # or mistral, phi, etc.
    temperature=0.7,
    base_url="http://172.16.1.224:11434"
)

# Chat
response = llm.invoke([
    HumanMessage(content="Explain transformers in simple terms")
])

print(response.content)