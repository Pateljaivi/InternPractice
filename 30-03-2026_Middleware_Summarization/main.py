from agent import AI_Agent

if __name__ == "__main__":
    bot = AI_Agent()
    user_id = "chat_user_1"

    print("--- Simple Chat Started (No DB) ---")
    while True:
        text = input("You: ")
        if text.lower() == "exit":
            break

        response = bot.run(user_id, text)
        print(f"AI: {response}")


