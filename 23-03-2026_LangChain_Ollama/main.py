from langchain_ollama import ChatOllama
#ChatOllama -> specific connector
from langchain_core.messages import HumanMessage
#HumanMessage ->  tool wraps your text into a format that the AI recognizes as a message coming from a human user

# Initialize model
llm = ChatOllama(
    model="llama3.2:latest",  # or mistral, phi, etc. #AI Brain
    temperature=0.7,#0.7 is a good balance for general conversation
    base_url="http://ai:11434",
)

# Chat
response = llm.invoke([
    HumanMessage(content="Explain transformers in simple terms")
])

print(response.content)