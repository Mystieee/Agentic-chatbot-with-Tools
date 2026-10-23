#this tool we will integrate with tavily search

from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools():
    """
    Return list of tools to be used in chatbot
    """
    tools = [TavilySearchResults(max_results = 2)]
    return tools

#convert tool to tool node
def create_tool_node(tools):
    """
    creates and return tool node for the graph
    """
    return ToolNode(tools=tools)
