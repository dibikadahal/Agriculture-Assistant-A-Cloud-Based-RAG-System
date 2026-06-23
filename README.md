# 🌾 Agriculture Assistant — A RAG-Powered Q&A System

A Retrieval-Augmented Generation (RAG) application that answers questions about
**sustainable farming practices** and **Nepal's agricultural statistics**, grounded
in real source documents. Built with LangChain, Google Gemini, ChromaDB, and Streamlit.

> Ask it *"Why is crop rotation beneficial?"* or *"What was the paddy production in Jhapa?"*
> — and it answers using actual documents, not the model's general knowledge.
>
---

## 📖 Overview

Large Language Models are powerful but have two limits: they don't know your
*private/specific* documents, and they can *hallucinate* facts. **RAG solves both**
by retrieving relevant text from your own documents and having the model answer
strictly from that retrieved context.

This project applies RAG to **agriculture**, combining two very different document types:

| Source | Type | Challenge solved |
|--------|------|------------------|
| FAO *Save and Grow* guide | Prose (farming practices) | Standard text chunking |
| *Statistical Information on Nepalese Agriculture 2080/81* | Tables & charts (data) | **Vision-based extraction** |

The statistical document is dominated by complex, multi-header **tables** and **bar charts**
that standard text extraction mangles. This project solves that using a **vision model**
that *reads the page as an image* — correctly interpreting grouped headers and even
estimating values from bar charts.

---

## ✨ Features

- **Multi-source retrieval** — answers from both a farming guide (prose) and government statistics (tabular) in one unified system.
- **Vision-based table & chart extraction** — uses Gemini's multimodal vision to read complex tables and bar charts that text parsers fail on, producing reliable, consistent data.
- **Grounded answers** — responses come from the source documents; the system says "I don't know" rather than hallucinating when information isn't present.
- **Source citations** — each answer can trace back to its source document and page number (stored as metadata).
- **Interactive web UI** — a clean, earthy-themed Streamlit chat interface with a collapsible info sidebar explaining the system and its data sources.

---

## 🛠️ Tech Stack

| Component | Tool | Role |
|-----------|------|------|
| Orchestration | **LangChain** | Wires retrieval + generation together |
| Embeddings | **Google `gemini-embedding-001`** | Turns text into searchable vectors |
| Vector database | **ChromaDB** | Stores and searches embeddings (cosine similarity) |
| LLM (generation) | **Google Gemini (`gemini-2.5-flash`)** | Writes answers from retrieved context |
| Vision extraction | **Gemini multimodal** | Reads tables & charts from PDF page images |
| PDF rendering | **pypdfium2** | Renders PDF pages to images |
| Table parsing | **pdfplumber** | Detects/extracts simple tables |
| Frontend | **Streamlit** | The chat web interface |

---

## 🧠 How It Works

```
                    ┌─────────────────  INGESTION (run once)  ─────────────────┐
                    │                                                          │
   PDF documents ──▶│  Load → Chunk / Vision-extract → Embed → Store           │──▶  ChromaDB
                    │  (prose split into chunks; tables & charts read by        │     (vectors)
                    │   a vision model, then converted to clean text)           │
                    └──────────────────────────────────────────────────────────┘

                    ┌─────────────────  QUERYING (every question)  ────────────┐
   Your question ──▶│  Embed question → Cosine-search ChromaDB → Top-k chunks   │
                    │       → Feed chunks + question to the LLM → Answer         │──▶  Answer
                    └──────────────────────────────────────────────────────────┘
```

1. **Retrieval** — your question is embedded into a vector and compared (via cosine
   similarity) against all stored document chunks; the most relevant ones are retrieved.
2. **Generation** — those retrieved chunks are passed to the LLM, which writes an
   answer grounded in them.

This separation is what makes answers both *fluent* (the LLM) and *factual* (the documents).

---

## 📂 Folder Structure

```
MyRAGProject/
│
├── app.py                  # Terminal version of the RAG Q&A
├── app_ui.py               # Streamlit web UI (main app)
│
├── ingest.py               # Ingests the prose PDF (Save and Grow)
├── ingest_stats.py         # Ingests statistical tables
├── ingest_charts.py        # Ingests bar charts via vision
├── vision_extract.py       # Vision-based extraction logic (tables/charts → text)
│
├── data/                   # Source PDFs (not tracked — see Data Sources below)
├── chroma_db/              # The vector database (auto-generated, not tracked)
├── images/                 # Rendered page images & screenshots
│
├── Test/                   # Experiment & learning scripts
│   ├── CosineSimilarityDemo.py
│   ├── view_embeddings.py
│   ├── test_tables.py
│   └── process_tables.py
│
├── .streamlit/
│   └── config.toml         # Streamlit theme (earthy color palette)
│
├── .env                    # API keys (NOT committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.12
- A **Google Gemini API key** — get one free at [Google AI Studio](https://aistudio.google.com/apikey)

### 1. Clone the repository
```bash
git clone https://github.com/dibikadahal/My-RAG-Project.git
cd My-RAG-Project
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API key
Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_api_key_here
```

### 5. Add the source documents
Download the PDFs into the `data/` folder (they're not tracked in git due to size):
- **Save and Grow (FAO):** https://www.fao.org/4/i2215e/i2215e.pdf
- **Statistical Information on Nepalese Agriculture 2080/81:** [Nepal MoALD](https://moald.gov.np/)

### 6. Build the knowledge base (run once)
```bash
python ingest.py          # ingest the prose guide
python ingest_stats.py    # ingest statistical tables
python ingest_charts.py   # ingest charts via vision
```
> ⚠️ The free Gemini tier has rate limits. Ingestion runs in batches with pauses to respect them.

### 7. Run the app
```bash
streamlit run app_ui.py
```
The app opens in your browser at `http://localhost:8501`.

---

## 💡 Example Questions

**Farming practices** (from the FAO guide):
- *What is conservation agriculture?*
- *Why is crop rotation beneficial?*
- *How can I improve soil health?*

**Statistics** (from the Nepal yearbook):
- *What was the paddy production in Jhapa?*
- *Which province produced the most maize in 2023/24?*
- *What was the total wheat production in Nepal?*

**From the chart data:**
- *Which legume fixes the most nitrogen?*

---

## 🧩 Key Technical Challenges Solved

**1. Tables and charts aren't text.**
A PDF stores tables as positioned text and charts as graphics — standard extraction
scrambles them. This project renders pages as images and uses a **vision model** to
interpret them correctly, including multi-tier headers and bar-chart values.

**2. Tables don't chunk like prose.**
Splitting a table by character count cuts rows in half. The solution: **linearize**
each row into a self-contained sentence (or let the vision model do it), so each
retrievable unit carries full context.

**3. Embedding model consistency.**
Queries must use the *same* embedding model that built the database, or vectors aren't
comparable. The project keeps embeddings on Gemini throughout for this reason.

---

## ⚠️ Limitations & Notes

- **Chart values are approximate** — read from bar heights, not printed numbers.
- **Free-tier rate limits** — the Gemini free tier caps daily requests; heavy testing may require waiting for resets or enabling billing.
- **Practice scope** — the statistical and chart ingestion currently covers a selected page range, easily expanded.
- **Nepali language** — the statistical PDF contains Nepali text; the multilingual embedding model handles it, with full bilingual support planned as a future enhancement.

---

## 🔮 Future Improvements

- Expand ingestion to the full statistical yearbook (all 224 pages).
- Add full Nepali-language query support.
- Per-row chunking of statistical data for sharper retrieval.
- Deploy to Streamlit Community Cloud for public access.

---

## 🙏 Acknowledgements

- **FAO** for the *Save and Grow* sustainable agriculture guide.
- **Nepal Ministry of Agriculture and Livestock Development (MoALD)** for the statistical data.
- Built with [LangChain](https://www.langchain.com/), [Google Gemini](https://ai.google.dev/), [ChromaDB](https://www.trychroma.com/), and [Streamlit](https://streamlit.io/).

---

*Built by [Dibika Dahal] — a project exploring Retrieval-Augmented Generation for real-world, multi-format documents.*

