from mongodb import save_message

def memory_tool(user_id:str, message:str):
    """
    only store tool,take decision by agent
    """

    save_message(user_id,message)

    return "Stored in MongoDB"
