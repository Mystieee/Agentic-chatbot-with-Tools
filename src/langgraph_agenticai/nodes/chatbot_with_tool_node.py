from src.langgraph_agenticai.state.state import State


class ChatbotWithToolNode:
    """
    Chatbot logic enhanced with Tool integration
    """

    def __init__(self, model):
        self.llm = model

    #invoke the llm based on the mesages
    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a response wth tool integration.
        """

        user_input = state["messages"][-1] if state["messages"] else ""
        llm_response = self.llm.invoke([{"role": "user", "content": user_input}])

        # simulate tool-specific logic
        tools_response = f"Tool integration fro: '{user_input}'"

        return {"messages": [llm_response, tools_response]}

    def create_chatbot(self, tools):
        """
        Returns a chatbot node function.
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            """
            chatbot logic for processing the input state and returning a response.
            """
            return {"messages": [llm_with_tools.invoke(state["messages"])]}

        return chatbot_node