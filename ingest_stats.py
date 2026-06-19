import time
import pdfplumber
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

load_dotenv()

# added the source to the pdf
pdf_path = "data/Statistical_Nepalese_Agriculture.pdf"
