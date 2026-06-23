import base64
import io
import pypdfium2 as pdfium
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

pdf_path = "data/SaveAndGrow.pdf"
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# Render the chart page (index 44)
pdf = pdfium.PdfDocument(pdf_path)
image = pdf[44].render(scale=2).to_pil()
image.save("images/legume_chart.png")