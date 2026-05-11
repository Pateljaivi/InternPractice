import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage, SystemMessage


class ChatBot:
    def __init__(self, model_name="llama-3.3-70b-versatile", temperature=0.3):

        """Initializes the LLM, tools, and conversation history."""

        load_dotenv()

        self.search_tool = TavilySearch(max_results=2)
        #TavilySearch->These are classes already provided by LangChain
        # This allows the chatbot to look up real-time info on the web
        self.tools = [self.search_tool]


        # Bind tools to the LLM
        self.llm = ChatGroq(
            model=model_name,
            temperature=temperature
        ).bind_tools(self.tools)


        # Initialize history with a system persona
        self.history = [SystemMessage(content="You are a helpful assistant.")]

    def _process_tool_calls(self, ai_msg):

        """Internal method to execute tools and return the final AI response."""

        self.history.append(ai_msg)


        #Sometimes an AI wants to search for two different things at once
        for tool_call in ai_msg.tool_calls:
            # Execute the tool and capture result
            result = self.search_tool.invoke(tool_call["args"])


            # Record the tool output in history
            self.history.append(ToolMessage(
                content=str(result),#The actual text found on the web
                tool_call_id=tool_call["id"]
                #a unique ID that links this specific answer to the specific question the AI asked
            ))


        # Call LLM again with the new tool context
        return self.llm.invoke(self.history)

    def ask(self, query):

        """Handles user input and manages the response loop."""

        self.history.append(HumanMessage(content=query))


        # Initial AI response check
        response = self.llm.invoke(self.history)


        # Loop tool processing if the model requests it
        if response.tool_calls:
            response = self._process_tool_calls(response)


        # Store final answer and return text
        self.history.append(AIMessage(content=response.content))

        return response.content


def start_interactive_chat():

    """Main function to run the chatbot in the terminal."""

    bot = ChatBot()
    print("--- AI Chatbot Ready (type 'exit' to quit) ---")


    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break


        answer = bot.ask(user_input)
        print(f"\nAI: {answer}")


if __name__ == "__main__":
    start_interactive_chat()

