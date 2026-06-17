from dotenv import load_dotenv #reads .env file and loads the GOOGLE_API_KEY
from langchain_community.document_loaders import PyPDFLoader #opens and loads the PDF
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings # converts text into a list of number that captures its meaning
from langchain_community.vectorstores import Chroma
import time

# load the API key from .env
load_dotenv()

# ======loading the PDF Document -> list of documents (one per page)=============
loader = PyPDFLoader("data/SaveAndGrow.pdf") #PyPDFLoader reads a single file
documents = loader.load()
print(documents[0].page_content)


#=========================CHUNKING THE TEXT===============================
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000, # each chunk splitted contains roughly 1000 characters
    chunk_overlap = 150 # each chunk repeats last 150 characters of the previous one
)
chunks = splitter.split_documents(documents)
print(f"Split into {len(chunks)} chunks.")


#=========CREATING EMBEDDINGS AND INITIALIZING THE VECTOR DB================
embeddings = GoogleGenerativeAIEmbeddings(model = "models/gemini-embedding-001") #t takes a raw text chunk and turns into a list of numbers with its conceptual meanings

vectorstore = Chroma(
    embedding_function = embeddings, # giving chroma the google tool it needs to convert those raw texts into numbers
    persist_directory = "chroma_db" # it saves the database to a chroma_db folder on disk.
)

#======Add chunks in small batches with pauses to respect the 100/min limit========
batch_size = 90
for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i + batch_size]
    vectorstore.add_documents(batch)
    print(f"Embedded {i + len(batch)} / {len(chunks)} chunks...")
    time.sleep(60)  # wait 60s between batches to stay under the per-minute cap

print(f"Done. Stored {len(chunks)} chunks in chroma_db/")