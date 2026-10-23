# design the page:

import streamlit as st
import os

from src.langgraph_agenticai.ui.uiconfigfile import Config

class LoadStreamlitUI:

    def __init__(self):
        self.config = Config()
        self.user_controls={}

    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 "+ self.config.get_page_title(), layout="wide")
        st.header("🤖 "+self.config.get_page_title())

        with st.sidebar:
            #get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            #llm selection
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == "Groq":
                #Model selection
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox("select Model", model_options)
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("API Key", type="password")

                #validate API Key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter your groq api key to proceed, Dont hav one ? refer: https://console.groq.com/keys")

            #usecase selection:
            self.user_controls["selected_usecases"] =st.selectbox("Select usecases", usecase_options)

            if self.user_controls["selected_usecases"] == "Chatbot with Web":
                os.environ["TAVILY_API_KEY"]= self.user_controls["TAVILY_API_KEY"] = st.session_state["tavily_api_key"] = st.text_input("TAVILY API KEY", type = "password")

                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please enter your tavily api key, Dont have one, please refer : https://app.tavily.com/home")
                    
            
        return self.user_controls







    
