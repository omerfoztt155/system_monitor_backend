# Much smaller than the root Dockerfile — the sensor only reads system
# stats and publishes them over MQTT, it never talks to Postgres or
# FastAPI, so it doesn't need any of those dependencies.
#
# Build context is still the project root (see docker-compose.yml:
# "context: .", "dockerfile: sensor/Dockerfile") because this needs
# files from backend/, mqtt/, and main.py at the repo root — not just
# the sensor/ folder itself.

FROM python:3.12-slim

WORKDIR /app

COPY sensor/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/__init__.py backend/__init__.py
COPY backend/logging_config.py backend/logging_config.py
COPY mqtt/ mqtt/
COPY sensor/ sensor/
COPY main.py .

CMD ["python", "main.py"]