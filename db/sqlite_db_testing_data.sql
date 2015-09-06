-- SQLite DB data for the flaskapis application.
--
-- To populate DB run command:
-- sqlite3 c:\personal\flaskapis\flaskapis.db < sqlite_db_testing_data.sql (Windows Development)
-- sqlite3 /home/wsgi/flaskapis/flaskapis.db < sqlite_db_testing_data.sql  (Linux Production)

DELETE FROM sensor;

-- sensor represents a remote device
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
  '4102 Drew Hill Lane, Chapel Hill, NC - USA',
  'UP',
  'DS18B20',
  'TEMPERATURE',
  'Dallas Semiconductor digital temperature sensor'            -- helps describe this sensor
);

DELETE FROM readings;

INSERT INTO readings (id, unit, value, utc, serial)
VALUES (1, "celsius", 11.69, "2015-01-06T20:19:55.597132+00:00", "000006c01f0b");
INSERT INTO readings (id, unit, value, utc, serial)
VALUES (2, "celsius", 12.69, "2015-02-06T20:19:55.597132+00:00", "000006c01f0b");
INSERT INTO readings (id, unit, value, utc, serial)
VALUES (3, "celsius", 13.69, "2015-03-06T20:19:55.597132+00:00", "000006c01f0b");
INSERT INTO readings (id, unit, value, utc, serial)
VALUES (4, "celsius", 14.69, "2015-04-06T20:19:55.597132+00:00", "000006c01f0b");
INSERT INTO readings (id, unit, value, utc, serial)
VALUES (5, "celsius", 15.69, "2015-05-06T20:19:55.597132+00:00", "000006c01f0b");
INSERT INTO readings (id, unit, value, utc, serial)
VALUES (6, "celsius", 16.69, "2015-06-06T20:19:55.597132+00:00", "000006c01f0b");
INSERT INTO readings (id, unit, value, utc, serial)
VALUES (7, "celsius", 17.69, "2015-07-06T20:19:55.597132+00:00", "000006c01f0b");
INSERT INTO readings (id, unit, value, utc, serial)
VALUES (8, "celsius", 18.69, "2015-08-06T20:19:55.597132+00:00", "000006c01f0b");
INSERT INTO readings (id, unit, value, utc, serial)
VALUES (9, "celsius", 19.69, "2015-09-06T20:19:55.597132+00:00", "000006c01f0b");
INSERT INTO readings (id, unit, value, utc, serial)
VALUES (10, "celsius", 20.69, "2015-10-06T20:19:55.597132+00:00", "000006c01f0b");

