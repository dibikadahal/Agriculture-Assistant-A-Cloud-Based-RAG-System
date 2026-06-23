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
