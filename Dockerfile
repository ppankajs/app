FROM python:3.10-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install curl and kubectl (specific version to avoid command substitution)
RUN apt-get update && \
    apt-get install -y curl ca-certificates gnupg && \
    curl -LO https://dl.k8s.io/release/v1.30.0/bin/linux/amd64/kubectl && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && \
    rm kubectl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY app.py .
COPY scripts/ /app/scripts/

# Expose Flask port
EXPOSE 5000

# Default command to run your Flask app
CMD ["python", "app.py"]
