from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain.agents.middleware import before_model, after_model, AgentState
from langchain.messages import AIMessage,HumanMessage
from langgraph.runtime import Runtime
from typing import Any


@before_model(can_jump_to=["end"])
def check_message_limit(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    if len(state["messages"]) >= 6:
        return {
            "messages": [AIMessage("Conversation limit reached.")],
            "jump_to": "end"
        }
    return None

@after_model
def log_response(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:

    return None

llm = ChatOllama(model="llama3.2:1b")

agent = create_agent(
    llm,
    tools=[],
    middleware=[check_message_limit, log_response]
)

history = []


print("--- Chat Started (Limit: 6 messages total) ---")
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    history.append(HumanMessage(content=user_input))

    response = agent.invoke({"messages": history})


    ai_msg = response["messages"][-1]
    history.append(ai_msg)

    print(f"AI: {ai_msg.content}")


    if "Conversation limit reached" in ai_msg.content:
        print("Session Ended")
        break