FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Librerías runtime mínimas para OpenCV/reportlab
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libgl1 libsm6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias
COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar archivos principales
COPY frontendApp.py ./frontendApp.py
COPY imgBack.png ./imgBack.png
COPY backend ./backend

# Copiar TODO el directorio yolo
COPY yolo ./yolo

# Copiar ejemplos si existen
COPY imgEjemplo ./imgEjemplo

# Config
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    DB_HOST=mysql \
    DB_PORT=3306 \
    DB_USER=root \
    DB_PASSWORD=1234 \
    DB_NAME=testrine

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "frontendApp.py", "--server.port=8501", "--server.address=0.0.0.0"]