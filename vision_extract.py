import pypdfium2 as pdfium # ypdfium2 talks directly to Google Chrome's C++ code and creates what is called a Bitmap.
import base64 # it takes binary data (like an image, PDF or an executable file) and convert it into a safe, clean string of text characters.
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import io
import time
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

pdf_path = "data/Statistical_Nepalese_Agriculture.pdf"
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

INSTRUCTION = (
    "Describe every table in this image. For each data row, write one sentence "
    "that includes the table title, the row's labels, and every value correctly "
    "paired with its column. Be precise with numbers. If there are no tables, reply 'NO TABLE'."
)

def extract_page_text(page_index):
    # render the page to an image
    pdf = pdfium.PdfDocument(pdf_path)
    image = pdf[page_index].render(scale=2).to_pil() # converts image stored in another format to Python Image Library
    image.save(f"images/page_{page_index}.png")

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

    message = HumanMessage(content=[
        {"type": "text", "text": INSTRUCTION},
        {"type": "image_url", "image_url": f"data:image/png;base64,{image_data}"}
    ])
    response = llm.invoke([message])
    return response.content

# Test the function on page 14
# print(extract_page_text(15))


# ================LOOP OVER ALL THE PAGES FROM 11 TO 25=================================
all_texts = []
all_metadata = []

for page_index in range(11,25): # page numbers 12 to 25
    print(f"Extracting page {page_index}")
    text = extract_page_text(page_index)

    if "NO TABLE" in text:
        print(f"Page {page_index} has no tables, skipped")
    else:
        all_texts.append(text)
        all_metadata.append({"page": page_index, "source": "Statistical_Nepalese_Agriculture"})
        print(f"  Page {page_index}: extracted {len(text)} characters.")

    time.sleep(5) # a 5-second gap between vision calls

print(f"\nDone. Extracted text from {len(all_texts)} pages.")


# ===========================WRAP TEXT WITH DOCUMENTS=================================
# Chroma stores Document objects, not raw strings.
# A Document bundles the text with its metadata (the page number), so the page citation
# travels with the data into the database.
documents = []

for text, meta in zip(all_texts, all_metadata):
    documents.append(Document(page_content = text, metadata = meta))

print(f"Created {len(documents)} Document objects.")


# =====================Embed and Store into Chroma DB====================================
# this is the final step — turn the documents into vectors and add them to your existing chroma_db (alongside SaveAndGrow).
# After this, app.py can answer statistical questions.
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory="chroma_db"     # SAME db as SaveAndGrow → merges in
)

# add in small batches with pauses
batch_size = 5
for i in range(0, len(documents), batch_size):
    batch = documents[i:i + batch_size] # extracts small group using list slicing (like: Document 0, 1, 2, 3, 4) at a time
    vectorstore.add_documents(batch) # This takes just that isolated batch of 5 documents, contacts the AI model to turn them into vector embeddings, and saves them into your Chroma database.
    print(f"Embedded {i + len(batch)} / {len(documents)} documents...")
    time.sleep(60)

print(f"Done. Added {len(documents)} statistical documents to chroma_db.")
