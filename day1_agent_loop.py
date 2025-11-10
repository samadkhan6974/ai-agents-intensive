def agent_decision(user_input):
    if "search" in user_input.lower():
        return "Agent would now perform a web search."
    elif "summarize" in user_input.lower():
        return "Agent would now summarize the text."
    else:
        return "Agent is thinking... no action required."

while True:
    user = input("You: ")
    if user.lower() == "exit":
        break
    print("Agent:", agent_decision(user))
