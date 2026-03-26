import os

def load_prompt(name):
    path = os.path.join("prompts", f"{name}.md")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()