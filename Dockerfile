FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Create Streamlit config
RUN mkdir -p ~/.streamlit && \
    echo "[server]\n\
headless = true\n\
port = ${PORT:-8501}\n\
enableCORS = false\n\
\n\
[theme]\n\
primaryColor = '#6366f1'\n\
backgroundColor = '#0f172a'\n\
secondaryBackgroundColor = '#1e293b'\n\
textColor = '#ffffff'\n\
font = 'sans serif'" > ~/.streamlit/config.toml

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=${PORT:-8501}", "--server.address=0.0.0.0"]
