# Stage 1: Builder Stage
FROM python:3.12-slim AS builder

# Install system dependencies for psycopg2 (if you want to use psycopg2 instead of psycopg2-binary)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev

# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY ./Requirements/requirements.txt /app/

# Install Python dependencies (including psycopg2 or psycopg2-binary)
RUN pip install --no-cache-dir -r /app/requirements.txt

# Install Gunicorn
RUN pip install gunicorn==23.0.0

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip
RUN pip install --upgrade pip

# Stage 2: Production Stage
FROM python:3.12-slim

# Create a non-root user and set app directory
RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

# Install Gunicorn
RUN pip install gunicorn==23.0.0

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/

# Set the working directory
WORKDIR /app

# Copy application code and set ownership
COPY --chown=appuser:appuser .. .

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "Config.wsgi:application"]