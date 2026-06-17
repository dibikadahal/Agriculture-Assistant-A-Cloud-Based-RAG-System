from dotenv import load_dotenv #reads .env file and loads the GOOGLE_API_KEY
from langchain_community.document_loaders import PyPDFLoader #opens and loads the PDF
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings # converts text into a list of number that captures its meaning
from langchain_community.vectorstores import Chroma


load_dotenv()

loader = PyPDFLoader("data/SaveAndGrow.pdf") #PyPDFLoader reads a single file
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000, # each chunk splitted contains roughly 1000 characters
    chunk_overlap = 150 # each chunk repeats last 150 characters of the previous one
)
chunks = splitter.split_documents(documents)

embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001") #this line just creates the embedding tool


vectorstore = Chroma.from_documents(
    documents = chunks,
    embedding = embeddings,
    persist_directory = "chroma_db"
)