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


# ======================The visible header page ===================================
st.title("🌾 Agriculture Assistant")
st.caption("Ask me about the farming practices and Nepal's agriculture statistics")

# ====================Initialize the chat history ====================================
# st.session_state is stored in your computer's RAM (memory)
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ====================Display the Chat History ====================================
# Loops through every stored message and displays it on screen as a chat bubble
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =======================Chat Input + Running the RAG ===============================
# := "walrus operator" - assigns the typed text to prompt and check if it's truthy
if prompt := st.chat_input("Ask your question related to agriculture here...."):
    # 1. Show and also store the user's message
    st.session_state.messgaes.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get answer from the RAG system
    with st.chat_message("assistant"):
        with st.spinner("Thinking....."):
            result = qa_chain.invoke({"query":prompt})
            answer = result["result"]
            st.markdown(answer)

    # 3. Store the assistant's answer
    st.session_state.messages.append({"role": "user", "content": answer})
