###############################################
# STAGE 1: Build and dependencies
###############################################
FROM python:3.13-slim-bullseye AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv using best practices
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

# Set uv configuration for better performance
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Create a minimal README.md file
RUN echo "# Provet API" > README.md

# Copy the application code
COPY provet/ /app/provet/
COPY api/ /app/api/
COPY data/ /app/data/
COPY scripts/ /app/scripts/

# Create necessary directories
RUN mkdir -p /app/solution /app/temp_uploads

###############################################
# STAGE 2: Testing
###############################################
FROM builder AS testing

# Copy test files
COPY tests/ /app/tests/
COPY pytest.ini /app/

# Install test dependencies
RUN uv sync --no-group dev --no-group api

# Run unit tests
RUN uv run pytest

###############################################
# STAGE 3: Runtime
###############################################
FROM python:3.13-slim-bullseye

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8000

# Copy application code from builder
COPY --from=builder /app /app

# Install necessary dependencies directly with pip
RUN pip install --no-cache-dir fastapi uvicorn python-multipart

# Install runtime dependencies and curl for healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install the application with its dependencies
RUN pip install --no-cache-dir -e .

# Create a non-root user
RUN useradd -m -u 1000 provet && \
    chown -R provet:provet /app

# Switch to non-root user
USER provet

# Expose the port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8000/ || exit 1

# Set the entrypoint
ENTRYPOINT ["uvicorn", "api.main:app", "--host", "0.0.0.0"]

# Default command
CMD ["--port", "8000"] 