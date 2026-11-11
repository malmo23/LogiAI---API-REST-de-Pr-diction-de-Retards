FROM python:3.11-slim
WORKDIR /app

# 1. Installer les dépendances d'abord (optimisation du cache Docker)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copier le code, les données et le modèle
COPY logiai/ ./logiai/
COPY data/ ./data/
COPY models/ ./models/

ENV LOGIAI_HOME=/app
EXPOSE 8000

CMD ["uvicorn", "logiai.api.main:app", "--host", "0.0.0.0", "--port", "8000"]