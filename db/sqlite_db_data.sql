-- SQLite DB data for the flaskapis application.
--
-- To populate DB run command:
-- sqlite3 c:\personal\flaskapis\flaskapis.db < sqlite_db_data.sql (Windows Development)
-- sqlite3 /home/wsgi/flaskapis/flaskapis.db < sqlite_db_data.sql  (Linux Production)


-- sensor represents a remote device
DELETE FROM sensor
WHERE serial="000006c01f0b";

INSERT INTO sensor (
  serial,
  geolocation,
  location,
  address,
  state,
  name,
  type,
  description
) VALUES (
  '000006c01f0b',
  '51.5033630,-0.1276250',
  'Living Room',
  '2800 BRAZOS BLVD, EULESS, TX - USA',
  'UP',
  'DS18B20',
  'TEMPERATURE',
  'Dallas Semiconductor digital temperature sensor'            -- helps describe this sensor
);


-- sensor represents a remote device
DELETE FROM sensor
WHERE serial="testing";

INSERT INTO sensor (
  serial,
  geolocation,
  location,
  address,
  state,
  name,
  type,
  description
) VALUES (
  'testing',
  '51.5033630,-0.1276250',
  'Living Room',
  '2800 BRAZOS BLVD, EULESS, TX - USA',
  'UP',
  'DS18B20',
  'TEMPERATURE',
  'Dallas Semiconductor digital temperature sensor'            -- helps describe this sensor
);