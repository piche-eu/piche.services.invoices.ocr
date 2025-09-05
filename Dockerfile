# Use a slim Python base image for smaller image size
FROM python:3.10-slim
RUN apt-get update && \
    apt-get install -y curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"
WORKDIR /app
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["uv", "fastmcp", "fastmcp.py"]