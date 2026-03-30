from agent import AI_Agent

if __name__ == "__main__":

    agent = AI_Agent()
    user_id = "user123"

    print("Chat started (type 'exit' to stop)")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        response = agent.run(user_id, user_input)

        print("AI:", response)
