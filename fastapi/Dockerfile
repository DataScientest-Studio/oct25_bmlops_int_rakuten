# ./fastapi/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY fastapi/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY fastapi/ /app/

CMD ["uvicorn", "etl_trigger:app", "--host", "0.0.0.0", "--port", "8001"]  # aktivieren, wenn Dateien für APIs fertig sind
