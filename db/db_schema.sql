-- Copyright (c) 2015 Rubens S. Gomes <rubens.s.gomes@gmail.com>
--
-- All Rights Reserved.

-- SQLite DB Schema for the flaskapis application.
--
-- To create DB run command:
-- sqlite3 c:\personal\flaskapis\flaskapis.db < db_schema.sql (Windows Development)
-- sqlite3 /home/wsgi/flaskapis/flaskapis.db < db_schema.sql  (Linux Production)


-- sensor represents a remote device
CREATE TABLE sensor (
  serial      TEXT PRIMARY KEY NOT NULL, -- unique manufacturer serial Id
  geolocation TEXT,           -- GEO Location: LATITUDE, LONGITUDE
  location    TEXT,           -- ENGINE, HOME, PATIO, ...
  address     TEXT,           -- Address where sensor is located
  state       TEXT NOT NULL,  -- UP, DOWN, ...
  name        TEXT NOT NULL,  -- name to help identify this sensor
  type        TEXT NOT NULL,  -- HUMIDITY, PRESSURE, TEMPERATURE, VELOCITY,  ...
  description TEXT            -- helps describe this sensor
);

-- data represents the sensor measurments
-- NOTE: SQLite does not have a DATETIME type.  We use TEXT instead.
CREATE TABLE readings (
  id          INTEGER PRIMARY KEY,  -- this column auto increments
  unit        TEXT NOT NULL, -- degC, degF, Kg, ....
  value       REAL NOT NULL, -- measured data
  utc         TEXT NOT NULL, -- ISO8601 UTC timestamp: "YYYY-MM-DD HH:MM:SS.SSS"
  serial      TEXT NOT NULL REFERENCES sensor(serial)
);