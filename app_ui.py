import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA # connect external database to an LLM allowing the model to answer questions using private, up-to-date, or specific documents rather than just its pre-trained knowledge
from dotenv import load_dotenv

from ingest import vectorstore

load_dotenv()

st.set_page_config(
    page_title = "Agriculture Assistant",
    page_icon = "🌾",
    layout = "centered"
)

# =============================The Cached RAG Engine===========================
@st.cache_resource
def load_rag_engine():
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/gemini-embedding-001")
    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function = embeddings
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k":4})
    llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature = 0.3)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

qa_chain = load_rag_engine()