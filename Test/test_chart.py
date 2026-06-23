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

# Encode it
buffer = io.BytesIO()
image.save(buffer, format="PNG")
image_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

# Chart-specific instruction
instruction = (
    "This image contains a bar chart titled 'Average amounts of nitrogen fixed "
    "by various legumes'. Read the chart carefully. For each legume (bar), estimate "
    "its value from the bar height against the Y-axis, and write one sentence per "
    "legume stating its approximate nitrogen fixation in kg N/ha/yr. List them clearly."
)

message = HumanMessage(content=[
    {"type": "text", "text": instruction},
    {"type": "image_url", "image_url": f"data:image/png;base64,{image_data}"}
])

response = llm.invoke([message])
print(response.content)