FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

EXPOSE 5000

COPY ./start_server.sh /app/start_server.sh

# Copy the application into the container.
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# RUN 

# Run the application.
CMD ["./start_server.sh"]
