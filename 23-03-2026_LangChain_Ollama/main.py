import os
from langchain_groq import ChatGroq  # Use ChatGroq instead of ChatOllama
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

# Initialize model
llm = ChatGroq(
    model="llama-3.3-70b-versatile", # One of Groq's most powerful models
    temperature=0.7,
    api_key=API_KEY # Paste your key here
)

# The logic stays exactly the same
response = llm.invoke([
    HumanMessage(content="Explain AI agents in simple terms")
])

print(response.content)