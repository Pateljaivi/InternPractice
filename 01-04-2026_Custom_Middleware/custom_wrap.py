from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.agents.middleware import before_model, wrap_model_call, AgentState, ModelRequest, ModelResponse
from langchain.messages import AIMessage, HumanMessage
from langgraph.runtime import Runtime
from typing import Any, Callable



@before_model(can_jump_to=["end"])
def check_message_limit(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    if len(state["messages"]) >= 4:
        return {
            "messages": state["messages"] + [AIMessage(content="Conversation limit reached.")],
            "jump_to": "end"
        }
    return None


@wrap_model_call
def retry_model(request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    for attempt in range(3):
        try:
            return handler(request)
        except Exception as e:
            if attempt == 2:
                raise e
            print(f"--- Attempt {attempt + 1} failed. Retrying... ---")
    return None



llm = ChatOllama(model="llama3.2:1b")

agent = create_agent(
    llm,
    tools=[],

    middleware=[check_message_limit, retry_model]
)


history = []
print("--- Chat Started (Limit: 4 | Retries: 3) ---")

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
        print("--- Session Ended ---")
        break