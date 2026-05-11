from langchain_ollama import ChatOllama
from langchain.agents import create_agent
import os
from dotenv import load_dotenv

load_dotenv()

from langgraph.checkpoint.mongodb import MongoDBSaver
from mongodb import client, save_message

class AI_Agent:
    def __init__(self):

        self.model = ChatOllama(model="llama3.2:1b")


        self.memory = MongoDBSaver(client, db_name="chat_checkpoints")


        self.agent = create_agent(
            model=self.model,
            tools=[],
            checkpointer=self.memory
        )

    def run(self, user_id, user_input):

        config = {"configurable": {"thread_id": user_id}}


        result = self.agent.invoke(
            {"messages": [("user", user_input)]},
            config=config
        )

        response_content = result["messages"][-1].content


        save_message(user_id, user_input)
        save_message("assistant", response_content)

        return response_content



