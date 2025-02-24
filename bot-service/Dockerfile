FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

EXPOSE 5000

# Copy the application into the container.
COPY . /app
COPY .env /app/.env

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

RUN uv run alembic upgrade head

# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "5000", "--host", "0.0.0.0"]