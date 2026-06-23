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

# ===================Applying the Earthy background using the CSS==============
st.markdown("""
<style>
.stApp {
    background: linear-gradient(160deg, #F7F1DE 0%, #DDC795 50%, #B89968 100%);
}
.stApp > header{
    background: transparent;
}
[data-testid="stMainBlockContainer"], 
[data-testid="stAppViewContainer"],
.main .block-container {
    background: transparent;
}

[data-testid="stChatMessage"] {
    background-color: #FBF6E9;
    border-radius: 18px;
    padding: 16px 20px;
    margin-bottom: 12px;
    border: 1px solid #A8895A;
    box-shadow: 0 3px 8px rgba(60, 45, 25, 0.25);
}
</style>
""", unsafe_allow_html=True) # injects raw CSS into the page.


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
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get answer from the RAG system
    with st.chat_message("assistant"):
        with st.spinner("Thinking....."):
            result = qa_chain.invoke({"query":prompt})
            answer = result["result"]
            st.markdown(answer)

    # 3. Store the assistant's answer
    st.session_state.messages.append({"role": "assistant", "content": answer})

# ===================================ADDING A SIDEBAR===================================
with st.sidebar:
    st.header("🌾 About")
    st.write(
        "This assistant answers questions about farming practices "
        "and Nepal's agricultural statistics, using real documents as its source."
    )

    st.divider()
    st.subheader("📚 Data Sources")
    st.markdown(
        "**1. Save and Grow (FAO)**  \n"
        "A guide on sustainable farming — soil health, crop rotation, "
        "conservation agriculture, and pest management.  \n"
        "[📄 View source](https://www.fao.org/4/i2215e/i2215e.pdf)\n\n"
        "**2. Statistical Information on Nepalese Agriculture 2080/81**  \n"
        "Official government data on crop area, production, and yield "
        "across Nepal's provinces and districts.  \n"
        "[📄 View source](https://giwmscdnone.gov.np/media/pdf_upload/Statistical%20Information%20on%20Nepalese%20Agriculture,%202080_81_a7s8aj4.pdf)"
    )

    st.divider()
    st.subheader("⚙️ How It Works")
    st.markdown(
        "**1. You ask** a question  \n"
        "**2. Search** — your question is matched against the documents "
        "to find the most relevant pieces  \n"
        "**3. Answer** — the AI reads those pieces and writes a response "
        "grounded in them"
    )
    st.caption(
        "This means answers come from the actual documents, "
        "not the AI's general knowledge."
    )

