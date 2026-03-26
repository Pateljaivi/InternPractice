import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyMuPDFLoader
from prompt import load_prompt

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "llama-3.1-8b-instant"

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0.3,
    max_tokens=1000
)


# ------------------ PDF ------------------
def extract_pdf(file_path):
    loader = PyMuPDFLoader(file_path)
    docs = loader.load()
    return "\n".join([doc.page_content for doc in docs])


# ------------------ PROMPTS ------------------
req_prompt = PromptTemplate.from_template(load_prompt("requirements"))
us_prompt = PromptTemplate.from_template(load_prompt("user_stories"))
task_prompt = PromptTemplate.from_template(load_prompt("generate_task"))

requirement_chain = req_prompt | llm
user_stories_chain = us_prompt | llm
tasks_chain = task_prompt | llm


# ------------------ TOOLS ------------------
@tool
def generate_requirements(text: str):
    """Generates a list of requirements from the provided text."""

    return requirement_chain.invoke({"text": text}).content


@tool
def generate_user_stories(requirements: str):
    """Converts business requirements into structured user stories."""
    return user_stories_chain.invoke({"requirements": requirements}).content


@tool
def generate_task(user_stories: str):
    """Breaks down user stories into specific actionable tasks. Generates only top 5-6 tasks."""
    return tasks_chain.invoke({"user_stories": user_stories}).content


tools = [generate_requirements, generate_user_stories, generate_task]

# ------------------ AGENT ------------------
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=load_prompt("agent_prompt")
)

# ------------------ RUN ------------------
if __name__ == "__main__":

    pdf_path = "ECommerce_SRS.pdf"

    print("Extracting PDF...")

    text = extract_pdf(pdf_path)[:5000]

    print(f"Text Extracted ({len(text)} chars). Running Agent...")

    try:
        result = agent.invoke(
            {
            "input": f"Analyze this SRS and generate ONLY the final technical tasks: {text}"
            }
        )

        print("\n===== FINAL TASKS =====\n")

        if "messages" in result:
            print(result["messages"][-1].content)
        else:
            print(result["output"])

    except Exception as e:
        print(f"Limit Hit...Error: {e}")




