import os
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()


llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0,
    base_url="http://127.0.0.1:11434"
)


tasks_db = []

@tool
def add_project_task(task_description: str) -> str:
    """Adds a new task to the project plan."""
    tasks_db.append(task_description)
    return f"SUCCESS: Added '{task_description}' to the project."

@tool
def get_final_summary() -> str:
    """Returns the list of all tasks created so far."""
    if not tasks_db:
        return "No tasks found."
    return "Project Todo List:\n" + "\n".join([f"- {t}" for t in tasks_db])


agent = create_agent(
    model=llm,
    tools=[add_project_task, get_final_summary],
    system_prompt=(
        "You are a Project Manager. Your job is to create a project plan. "
        "Use the 'add_project_task' tool for EACH step the user asks. "
        "After adding ALL tasks, use 'get_final_summary' to show the complete list. "
    ),
    middleware=[TodoListMiddleware()],
)


print("--- Project Manager Agent Starting ---")


user_query = (
    "I want to start a Python project. Please do these 3 steps: "
    "1. Add a task to 'Setup Virtual Environment'. "
    "2. Add a task to 'Install LangChain and Ollama'. "
    "Finally, show me the full project summary."
)

try:
    response = agent.invoke(
        input={"messages": [{"role": "user", "content": user_query}]}
    )

    print("\n--- AGENT'S FINAL OUTPUT ---")
    print(response["messages"][-1].content)

except Exception as e:
    print(f"Error: {e}")



