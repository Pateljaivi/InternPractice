import os, pdfplumber
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
    api_key=os.getenv("GROQ_API_KEY")
)

def tool_1_requirements(text):

    prompt =  (
              "Extract Functional & Non-Functional requirements from this SRS."
              "Format: Use ## Headers and bullet points."
    )
    print("Running Tool 1...")
    res = llm.invoke([("system", prompt), ("human", text)])
    return res.content


def tool_2_stories(reqs):

    prompt = (
          "Convert requirements into User Stories."
          "Format: Create a Markdown table with columns: | Title | Description | Acceptance Criteria |."
    )
    print("Running Tool 2...")
    res = llm.invoke([("system", prompt), ("human", reqs)])
    return res.content


def tool_3_tasks(stories):
    # Medium Prompt for Task Assignment
    prompt = (
              "Break these stories into technical tasks."
              "Categorize by: Frontend, Backend, and QA for each story ID."
    )
    print("Running Tool 3...")
    res = llm.invoke([("system", prompt), ("human", stories)])
    return res.content


pdf_path = "ecommerce_srs.pdf"

if os.path.exists(pdf_path):

    with pdfplumber.open(pdf_path) as pdf:
        raw_text = "".join([p.extract_text() for p in pdf.pages])


    out1 = tool_1_requirements(raw_text)
    with open("Requirements.md", "w", encoding="utf-8") as f: f.write(out1)

    out2 = tool_2_stories(out1)
    with open("User_Stories.md", "w", encoding="utf-8") as f: f.write(out2)

    out3 = tool_3_tasks(out2)
    with open("Tasks.md", "w", encoding="utf-8") as f: f.write(out3)

    print("\nSuccess! separate files generated.")
else:
    print("Error: PDF file not found!")
