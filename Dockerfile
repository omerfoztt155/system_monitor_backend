# Shared image for the "api" and "listener" services — same codebase,
# they just run different commands (see docker-compose.yml). Not used
# by the "sensor" service, which has its own, much smaller Dockerfile.

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ backend/
COPY mqtt/ mqtt/
COPY api/ api/
COPY run_backend.py .

EXPOSE 8000

# Default command = run the API. The "listener" service overrides this
# with `command: python run_backend.py` in docker-compose.yml.
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]