# all components will be called step by step using this file

import streamlit as st
from src.langgraph_agenticai.LLMS.groqllm import GroqLLM
from src.langgraph_agenticai.graph.graph_builder import GraphBuilder

from src.langgraph_agenticai.ui.streamlit.loadui import LoadStreamlitUI
from src.langgraph_agenticai.ui.streamlit.display_result import DisplayResultStreamlit



def load_langraph_agentic_ai_app():
    """
    Loads and runs the Lang Graph Agenic AI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLM model,
    sets up the graph based on the selected use case and displays the output while
    implementing exception handling for robustness.
    
    """

    ## Load uI
    ui = LoadStreamlitUI()

    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from ui..")
        return

    user_message = st.chat_input("Enter your message: ")

    if user_message:
        try:
            #configure llm
            obj_llm_config = GroqLLM(user_controls_input = user_input)
            model = obj_llm_config.get_llm_models()

            if not model:
                st.error("Error: LLM model could not be initialized.")
                return

            #initialize and setup the graph based on use case
            usecase = user_input.get("selected_usecases")
            if not usecase:
                st.error("Error: no use case selected.")
                return

            #Graph builder:
            graph_builder = GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Graph setup failed..{e}")
                return
            
        except Exception as e:
            st.error(f"Error: Graph failed {e}")
            return


