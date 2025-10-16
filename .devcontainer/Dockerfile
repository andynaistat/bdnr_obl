FROM python:3.11-slim

ENV PIP_NO_CACHE_DIR=1
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/app
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# Extensiones de VS Code se configuran en devcontainer.json
