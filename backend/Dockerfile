FROM python:3.13-slim-bookworm AS builder

WORKDIR /app

# Install uv via pip to guarantee compatibility
RUN pip install --no-cache-dir uv

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy Python package metadata
COPY pyproject.toml ./

# Install dependencies using uv sync (no dev dependencies)
RUN uv sync --no-install-project --no-dev

# Second stage for a clean, secure, and minimal production image
FROM python:3.13-slim-bookworm

WORKDIR /app

# Copy virtualenv and compiled dependencies
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy FastAPI backend application code
COPY app /app/app

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
