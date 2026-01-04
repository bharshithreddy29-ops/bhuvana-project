FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for OpenCV and other libs
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-ml.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-ml.txt

COPY . .

# Create necessary directories
RUN mkdir -p static/images/uploads static/images/products datasets

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
