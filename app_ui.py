import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA # connect external database to an LLM allowing the model to answer questions using private, up-to-date, or specific documents rather than just its pre-trained knowledge
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title = "Agriculture Assistant",
    page_icon = "🌾",
    layout = "centered"
)