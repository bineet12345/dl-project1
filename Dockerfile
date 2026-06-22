FROM python:3.10-slim-bullseye

WORKDIR /app

# Copy files into the container
COPY . /app

# Upgrade pip and install everything (including awscli) via pip cleanly
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt awscli

CMD ["python3", "app.py"]