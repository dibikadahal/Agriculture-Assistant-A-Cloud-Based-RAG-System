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


# this code extracts one page's table into sentence
all_sentences = []
all_metadata = [] # this is used to remember from which page the sentence came.

with pdfplumber.open(pdf_path) as pdf:
    for page_index in range(11, 25):
        page = pdf.pages[page_index]
        text = page.extract_text() or ""
        title = text.split("\n")[0]
        tables = page.extract_tables()

        for table in tables:
            if not table or len(table) < 2: # this means skip empty tables ot those tables which only contains headers
                continue
            header = table[0]
            for row in table[1:]:
                sentence = row_to_sentence(header, row, title)
                if sentence is not None:
                    all_sentences.append(sentence)
                    all_metadata.append({"page": page_index, "source": "Statistical_Nepalese_Agriculture"})

print(f"Total sentences from pages 11-24: {len(all_sentences)}")
print("\nFirst sentence:", all_sentences[0])
print("Last sentence:", all_sentences[-1])
