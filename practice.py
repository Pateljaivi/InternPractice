import os
from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()


BASE_URL = os.getenv("BASE_URL")

# Initialize model
llm = ChatOllama(
    model="mistral-nemo",
    base_url=BASE_URL,
)


response = llm.invoke([
    HumanMessage(content="Explain AI agents in simple terms")
])

print(response.content)


