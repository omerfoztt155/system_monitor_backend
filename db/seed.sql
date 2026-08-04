-- Minimal dev data so the app is usable right after schema.sql runs.
-- main.py's Sensor("laptop-01") won't produce any stored metrics unless
-- a matching device row already exists — without this, every reading
-- gets rejected with DeviceNotFoundError.
--
--   psql -U postgres -d iot_backend -f db/seed.sql

INSERT INTO devices (device_code, location)
VALUES ('laptop-01', 'home')
ON CONFLICT (device_code) DO NOTHING;