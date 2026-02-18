# Multi-stage build for NEXIS Backend
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application
COPY . .

# Make sure scripts are executable
RUN chmod +x train_model.py

# Train model during build (optional - can be done at runtime)
RUN python train_model.py

# Expose port
EXPOSE 8000

# Set environment
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
