from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import numpy as np

load_dotenv()
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# The cosine similarity formula in code:
def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    #      dot product   /   (length of a  ×  length of b)

# Embed three phrases
v1 = embeddings.embed_query("soil fertility and crop nutrients")
v2 = embeddings.embed_query("how to keep farmland healthy")    # similar meaning
v3 = embeddings.embed_query("the price of a mobile phone")      # unrelated

print("soil vs farmland (similar → HIGH):", cosine_similarity(v1, v2))
print("soil vs phone    (unrelated → LOW):", cosine_similarity(v1, v3))