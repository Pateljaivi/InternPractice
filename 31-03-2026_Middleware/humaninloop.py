import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_agent

load_dotenv()



@tool
def post_to_social_media(content: str, platform: str) -> str:
    """Useful to post content to social media. Required for sharing."""
    return f"SUCCESS: Posted to {platform}: {content}"



llm = ChatOllama(model="llama3.2:1b", temperature=0)
memory = MemorySaver()


agent = create_agent(
    llm,
    tools=[post_to_social_media],
    checkpointer=memory,
    interrupt_before=["tools"]
)


def run_hitl():
    config = {"configurable": {"thread_id": "hitl_1"}}
    print("\n--- Fast HITL Manager ---")

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]: break


        for event in agent.stream({"messages": [HumanMessage(content=user_input)]}, config):
            pass


        snapshot = agent.get_state(config)
        if snapshot.next:
            print("\n [APPROVAL REQUIRED]: AI is trying to post something!")
            choice = input("Approved ? (y/n): ").lower()

            if choice == 'y':
                # Resume execution
                for event in agent.stream(None, config): pass
            else:
                print("Action Rejected.")
                continue

        # Final Reply
        final_state = agent.get_state(config)
        print(f"AI: {final_state.values['messages'][-1].content}")


if __name__ == "__main__":
    run_hitl()


