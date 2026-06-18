from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model = "models/gemini-embedding-001")

vectorstore = Chroma(
    persist_directory = "chroma_db",
    embedding_function = embeddings
)