FROM python:3.11-slim

WORKDIR /app

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# API-Code
COPY api/ /app/api/

# utils & other code
COPY src/ /app/src/

ENV PYTHONPATH=/app/src

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8001"]