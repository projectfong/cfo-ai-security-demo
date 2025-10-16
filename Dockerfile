# -------------------------------------------------------
# Dockerfile
# -------------------------------------------------------
# Author: projectfong
# Copyright (c) 2025 Fong
# All Rights Reserved
# -------------------------------------------------------
FROM python:3.11-slim
RUN useradd -m demo && mkdir -p /evidence && chown demo:demo /evidence
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chown -R demo:demo /app /evidence
USER demo
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
