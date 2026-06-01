# Cloud Run-specific image for the controlled Alpha Solver MVP preview.
# The legacy infrastructure/Dockerfile is a generic placeholder image; this
# root Dockerfile starts the FastAPI app and honors Cloud Run's PORT contract.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "exec python -m uvicorn service.app:app --host 0.0.0.0 --port \"${PORT:-8080}\""]
