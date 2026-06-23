from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import RetrievalQA

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model = "models/gemini-embedding-001")

vectorstore = Chroma(
    persist_directory = "chroma_db",
    embedding_function = embeddings
)

#============Configure the Database to act as a document retriever===========
# "given a question, return the most relevant chunks."
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

#==============================Setting up the LLM=================================
# the chat model that actually writes answers.
llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash", temperature = 0.3)

#================Chains the LLM and Retriever together============================
# Builds the actual RAG pipeline by connecting your retriever to your LLM
qa_chain = RetrievalQA.from_chain_type(
    llm = llm,
    chain_type = "stuff",
    retriever = retriever,
    return_source_documents = True
)

#=============Ask questions to the model in a loop==============================
print ("Ask about the document! (type 'quit' to exit)\n")

#====================Ask question in a loop=====================================
# this block lets you type questions and get answers, repeatedly, until you type quit.
while True:
    question = input("Question: ")
    if question.lower() == "quit":
        break
    result = qa_chain.invoke({"query": question})
    print("\nAnswer:", result["result"])
    print("-" * 50)
