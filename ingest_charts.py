# this file focuses on the charts from page index 43-46 from Save and Grow pdf

import base64
import io
import time
import pypdfium2 as pdfium
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()


pdf_path = "data/SaveAndGrow.pdf"
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

INSTRUCTION = (
    "This is a page from an agriculture book that may contain charts, graphs, "
    "or diagrams. If it has a chart or graph, read it carefully: for each data "
    "point or bar, estimate its value from the axis and write a clear sentence "
    "stating what it shows. Include the chart's title. If there is no chart or "
    "graph on this page, reply only 'NO CHART'."
)


# ==============The render and vision function============================
def extract_chart_text(page_index):
    # Render the page to an image
    pdf = pdfium.PdfDocument(pdf_path)
    image = pdf[page_index].render(scale=2).to_pil()
    image.save(f"images/saveandgrow_page_{page_index}.png")

    # Encode the image
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Send image + instruction to the vision model
    message = HumanMessage(content=[
        {"type": "text", "text": INSTRUCTION},
        {"type": "image_url", "image_url": f"data:image/png;base64,{image_data}"}
    ])
    response = llm.invoke([message])
    return response.content