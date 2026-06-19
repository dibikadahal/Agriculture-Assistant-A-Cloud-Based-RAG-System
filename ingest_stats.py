import time
import pdfplumber
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

load_dotenv()

# added the source to the pdf
pdf_path = "data/Statistical_Nepalese_Agriculture.pdf"

# the generic row-to-sentence function already tested in process_tables.py
def row_to_sentence(header, row, title):
    parts = []
    for col_name, value in zip(header, row):
        if value is not None and col_name is not None:
            parts.append(f"{col_name}: {value}")
    if len(parts) < 2:
        return None
    return f"From '{title}' — " + ", ".join(parts) + "."