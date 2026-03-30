from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import MemorySaver
import os
from dotenv import load_dotenv

load_dotenv()



class AI_Agent:
    def __init__(self):

        self.model = ChatOllama(model="llama3.2:1b")


        self.memory = MemorySaver()


        self.agent = create_agent(
            model=self.model,
            tools=[],
            checkpointer=self.memory,
            middleware=[
                SummarizationMiddleware(
                    model=self.model,
                    trigger=("messages", 6),  # Summarize after 6 messages
                    keep=("messages", 2),  # Always keep last 2 messages exact
                )
            ]
        )

    def run(self, user_id, user_input):

        config = {"configurable": {"thread_id": user_id}}


        result = self.agent.invoke(
            {"messages": [("user", user_input)]},
                  config=config
        )

        return result["messages"][-1].content

