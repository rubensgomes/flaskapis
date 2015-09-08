"""rgapps.dao.sqlitesensor module

This is where all the SQLite sensor database code is placed.
"""


import logging
import sqlite3

from rgapps.config import ini_config
from rgapps.utils.utility import dict_factory


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["SQLiteSensor"]


class SQLiteSensor:
    """ Class to provide sensor SQLite database API code
    """

    @staticmethod
    def add_reading(unit, value, utc, serial):
        """
        Adds given measurement data to sensor database

        Parameters
        ----------
        unit:  str (required)
            degF, degC, degF.
        value:  float (required)
            a float number
        utc: str (required)
            UTC timestamp of the reading
        serial: str (required)
            sensor unique serial number

        Returns
        -------
            nothing.
        """
      
        sql_db = ini_config.get("SqlLite", "SQLITE_DB")
        conn = sqlite3.connect(sql_db)
        logging.debug("Connected to SQLite DB [{0}]".format(sql_db))

        c = conn.cursor()
        c.execute("INSERT INTO readings (id, unit, value, utc, serial) "
                  "VALUES (?,?,?,?,?)",
                  (None, unit, value, utc, serial))

        conn.commit()
        logging.debug("Measurement has been committed in SQLite database")
        conn.close()

        logging.debug("Disconnected from SQLite DB [{0}]".format(sql_db))

        return

    @staticmethod
    def del_readings(serial):
        """
        Deletes all measurement data for the given serial

        Parameters
        ----------
        serial: str (required)
            sensor unique serial number

        Returns
        -------
            nothing.
        """

        logging.debug("Deleting all measurements in SQLite database for "
                      "serial [{0}]".format(serial))

        sql_db = ini_config.get("SqlLite", "SQLITE_DB")
        conn = sqlite3.connect(sql_db)
        logging.debug("Connected to SQLite DB [{0}]".format(sql_db))

        c = conn.cursor()
        c.execute("DELETE FROM readings WHERE serial = '{0}' "
                   .format(serial))

        conn.commit()
        logging.debug("Measurements have been deleted from SQLite database")
        conn.close()

        logging.debug("Disconnected from SQLite DB [{0}]".format(sql_db))

        return


    @staticmethod
    def get_readings(serial, current_datetime, past_datetime):
        """
        Returns .....

        Parameters
        ----------
        serial: str (required)
            sensor unique serial number
        current_datetime: str (required)
            a valid UTC timestamp
        past_datetime: str (required)
            a valid UTC timestamp

        Returns
        -------
        dict:
            A sensor dictionary containing column names as keys, and
            corresponding values.
        """

        logging.debug("Retrieving readings from sensor with serial [{0}] "
                       "between [{1}] and [{2}] from SQLite database."
                      .format(serial, past_datetime, current_datetime))

        sql = ("SELECT utc, serial, unit, value FROM readings WHERE serial = '{0}' "
               "AND utc BETWEEN '{1}' AND '{2}' "
               "ORDER BY utc ASC"
               .format(serial, past_datetime, current_datetime))

        sql_db = ini_config.get("SqlLite", "SQLITE_DB")
        conn = sqlite3.connect(sql_db)
        logging.debug("Connected to SQLite DB [{0}]".format(sql_db))

        c = conn.cursor()
        c.row_factory = dict_factory
        cursor = c.execute(sql)
        data = cursor.fetchall()

        conn.commit()
        conn.close()

        logging.debug("Disconnected from SQLite DB [{0}]".format(sql_db))

        return data


    @staticmethod
    def add_sensor(serial, geolocation, location, address, state, name,
                    sensor_type, description):
        """
        Adds given sensor data to sensor database

        Parameters
        ----------
        serial:  str (required)
            sensor unique serial number.
        geolocation:  str (optional)
            GEO Location: LATITUDE, LONGITUDE 
        location: str (optional)
            ENGINE, HOME, PATIO, ...
        address: str (optional)
            Address where sensor is located
        state: str (required)
            UP, DOWN, ...
        name: str (required)
            name to help identify this sensor
        sensor_type: str (required)
            HUMIDITY, PRESSURE, TEMPERATURE, VELOCITY,  ...
        description: str(optional)
            helps describe this sensor

        Returns
        -------
            nothing.
        """

        logging.debug("Inserting sensor in SQLite database: "
                      "serial [{0}], state [{1}], name [{2}], type [{3}]"
                      .format(serial, state, name, sensor_type))

        sql_db = ini_config.get("SqlLite", "SQLITE_DB")
        conn = sqlite3.connect(sql_db)
        logging.debug("Connected to SQLite DB [{0}]".format(sql_db))

        c = conn.cursor()

        c.execute("INSERT INTO sensor ( serial, geolocation, location, "
                    " address, state, name, type, description ) "
                  "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (serial, geolocation, location, address, state, name,
                    sensor_type, description))

        conn.commit()
        logging.debug("sensor has been committed in database")
        conn.close()

        logging.debug("Disconnected from SQLite DB [{0}]".format(sql_db))

        return


    @staticmethod
    def del_sensor(serial):
        """
        Deletes sensor data for the given serial

        Parameters
        ----------
        serial: str (required)
            sensor unique serial number

        Returns
        -------
            nothing.
        """

        logging.debug("Deleting sensor in database for "
                      "serial [{0}]".format(serial))

        sql_db = ini_config.get("SqlLite", "SQLITE_DB")
        conn = sqlite3.connect(sql_db)
        logging.debug("Connected to SQLite DB [{0}]".format(sql_db))

        c = conn.cursor()
        c.execute("DELETE FROM sensor WHERE serial = '{0}' "
                   .format(serial))

        conn.commit()
        logging.debug("Sensor has been deleted from database")
        conn.close()

        logging.debug("Disconnected from SQLite DB [{0}]".format(sql_db))

        return


    @staticmethod
    def get_sensor(serial):
        """
        Returns a tuble corresponding to the sensor table in the database
        for the given sensor serial.

        Parameters
        ----------
        serial: str (required)
            sensor unique serial number

        Returns
        -------
        dict:
            A sensor dictionary containing column names as keys, and
            corresponding values.
        """

        logging.debug("Retrieving sensor with serial [{0}] from database."
                      .format(serial))

        sql_db = ini_config.get("SqlLite", "SQLITE_DB")
        conn = sqlite3.connect(sql_db)
        logging.debug("Connected to SQLite DB [{0}]".format(sql_db))

        c = conn.cursor()
        c.row_factory = dict_factory
        cursor = c.execute(("SELECT * FROM sensor WHERE serial = '{0}'"
                             .format(serial)))
        data = cursor.fetchone()

        conn.commit()
        conn.close()

        logging.debug("Disconnected from SQLite DB [{0}]".format(sql_db))

        return data

