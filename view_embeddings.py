from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma


load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

db = Chroma(
    embedding_function=embeddings,
    persist_directory="chroma_db"
)

# pull stored chunks and their embeddings
data = db.get(include = ["documents", "embeddings"])

texts = data["documents"]
vectors = data["embeddings"]

# Look at the first chunk
print("===== CHUNK 0 TEXT =====")
print(texts[0][:200])          # first 200 chars of the text

print("\n===== CHUNK 0 EMBEDDING =====")
print("Vector length (dimensions):", len(vectors[0]))   # how many numbers
print("First 20 numbers:", vectors[5][:20])             # preview the vector
print("Full vector:", vectors[0])                       # the entire thing

