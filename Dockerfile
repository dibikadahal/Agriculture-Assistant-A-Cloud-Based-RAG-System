FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app_ui.py .
COPY .streamlit/config.toml .streamlit/config.toml
COPY chroma_db/ chroma_db/

# Cloud Run / most hosts pass the port in $PORT; default to 8501 locally
ENV PORT=8501
EXPOSE 8501

CMD ["streamlit", "run", "app_ui.py", "--server.address=0.0.0.0", "--server.port=8501"]
