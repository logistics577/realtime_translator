# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose (Render replaces this dynamically)
EXPOSE 8000

# Run Uvicorn on Render-assigned PORT
CMD ["sh", "-c", "uvicorn stream:app --host 0.0.0.0 --port $PORT"]
