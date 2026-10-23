from langgraph.graph import StateGraph, START, END
from src.langgraph_agenticai.state.state import State
from src.langgraph_agenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraph_agenticai.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition
from src.langgraph_agenticai.nodes.chatbot_with_tool_node import ChatbotWithToolNode

class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)


    def basic_chatbot_build_graph(self):
        """
        Building a basic chatbot graph using LangGraph.
        Tis method initializes a chatbot node using the 'BasicChatbotNode' class
        and integrates it into the graph. The chatbot node is set as both the
        entry and exit point of the graph.
        """

        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)


    def chatbot_with_tools_build_graph(self):
        """
        Builds an advanced chatbot graph with tool integration.
        This method creates a chatbot graph that includes both a chatbot node
        and a tool node. It defines tools, initializes the chatbot with  toolcapabilities,
        and setup conditional and direct edges between nodes. 
        The chatbot node is set as the entry point.
        """

        ## Define the tool and tool node
        tools = get_tools()
        tool_node = create_tool_node(tools)

        # define the llm
        llm = self.llm

        #define the chatbot node
        obj_chatbot_node = ChatbotWithToolNode(llm)
        chatbot_node = obj_chatbot_node.create_chatbot(tools)



        #Add node
        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        #define conditional edge and notmal edge
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)


    def setup_graph(self, usecase: str):
        #it will decide, which fn to cALL based on a aspecific usecase
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot with Web":
            self.chatbot_with_tools_build_graph()

        return self.graph_builder.compile()
        