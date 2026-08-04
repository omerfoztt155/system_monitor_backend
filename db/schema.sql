-- Creates the tables this application expects. Run once against a fresh
-- database:
--
--   psql -U postgres -d iot_backend -f db/schema.sql
--
-- Safe to re-run: every statement uses IF NOT EXISTS.

CREATE TABLE IF NOT EXISTS devices (
    id           SERIAL PRIMARY KEY,
    device_code  VARCHAR(100) NOT NULL UNIQUE,
    location     VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS system_metrics (
    id           SERIAL PRIMARY KEY,
    device_id    INTEGER NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
    cpu_usage    NUMERIC(5, 2) NOT NULL CHECK (cpu_usage BETWEEN 0 AND 100),
    ram_usage    NUMERIC(5, 2) NOT NULL CHECK (ram_usage BETWEEN 0 AND 100),
    disk_usage   NUMERIC(5, 2) NOT NULL CHECK (disk_usage BETWEEN 0 AND 100),
    received_at  TIMESTAMP NOT NULL DEFAULT now()
);

-- The service layer always looks up a metric's device by device_id, and
-- the API/dashboard always reads metrics ordered by time — index both.
CREATE INDEX IF NOT EXISTS idx_system_metrics_device_id ON system_metrics (device_id);
CREATE INDEX IF NOT EXISTS idx_system_metrics_received_at ON system_metrics (received_at DESC);