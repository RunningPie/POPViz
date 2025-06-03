# ===== Stage 1: Build Stage =====
FROM python:3.12-slim AS builder

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install --no-cache-dir -r requirements.txt

WORKDIR /build
COPY app ./app
COPY ML ./ML

# ===== Stage 2: Final Stage =====
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed pip packages
COPY --from=builder /install /usr/local

# Tell Python where to find them
ENV PYTHONPATH=/usr/local/lib/python3.12/site-packages

# Copy app source code
COPY --from=builder /build/app ./app
COPY --from=builder /build/ML ./ML

CMD ["python", "app/main.py"]
