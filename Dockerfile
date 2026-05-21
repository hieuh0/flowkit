FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (ffmpeg for video concat)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agent/ ./agent/

# Default WS port matches docker-compose.yml mapping
ENV WS_PORT=9222

# Expose API + WebSocket ports
EXPOSE 8100 9222

CMD ["python", "-m", "agent.main"]
