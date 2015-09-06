"""rgapps.dao.sensordao module

This is where all the sensor database code is placed.
"""
import logging
import sqlite3

import arrow
from pymongo import MongoClient
import pymongo

from rgapps.config import ini_config
from rgapps.utils.enums import DURATION_ENUM
from rgapps.utils.exception import IllegalArgumentException
from rgapps.utils.utility import dict_factory, is_blank, is_number


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["SensorDAO"]

# PRIVATE USE ONLY
class _SensorSQLite:
    """ Private class to provide sensor SQLite database API code
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



# PRIVATE USE ONLY
class _SensorMongoDB:
    """ Private class to provide sensor MongoDB database API code
    """

    @staticmethod
    def _get_mongodb_client():
        """
        Returns a valid and connected MongoClient object.

        Returns
        -------
        A MongoClient instance.

        Raises
        ------
        Raises MongoDB exception if MongoDB is not up and running, and the
        client could NOT connect to the database
        """

        # do not wait to connect to the server
        client = MongoClient(serverSelectionTimeoutMS=0)

        # run following call to check the server is up and running
        info = client.server_info()

        logging.debug("Connected to MongoDB [{0}] version [{1}] on OS [{2}]."
                      .format(client, info["version"], info["targetMinOS"]))

        return client


    @staticmethod
    def _get_mongodb(name):
        """
        Returns a valid and connected Mongo Database object.

        Parameters:
        ----------
        name: str (required)
            the name of the MongoDB database

        Returns
        -------
        A Mongo Database instance.

        Raises
        ------
        Raises MongoDB exception if MongoDB is not up and running, and the
        client could NOT connect to the database
        """

        client = _SensorMongoDB._get_mongodb_client()

        db_found = False
        dbs = client.database_names()

        for db_name in dbs:
            if (db_name == name):
                db_found = True
                break

        if not db_found:
            client.close()
            raise IllegalArgumentException("MongoDB DB name [{0}] not found!"
                                           .format(name))

        db = client['{0}'.format(name)]

        logging.debug("MongoDB with database name [{0}] found."
                      .format(name))

        return db


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

        mongodb_name = ini_config.get("MongoDB", "MONGO_DB")
        db = _SensorMongoDB._get_mongodb(mongodb_name)

        coll = db['readings']

        result = coll.insert_one({"unit": unit,
                                  "value": value,
                                  "utc": utc,
                                  "serial": serial
                                 })

        logging.debug("Sensor reading with id [{0}] has been inserted "
                      "into MongoDB database"
                      .format(result.inserted_id))

        db.client.close()

        logging.debug("Disconnected from MongoDB")

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

        mongodb_name = ini_config.get("MongoDB", "MONGO_DB")
        db = _SensorMongoDB._get_mongodb(mongodb_name)

        coll = db['readings']

        logging.debug("Deleting all readings in the MongoDB collection [{0}] "
                      "for sensor serial [{1}]."
                      .format(coll, serial))

        result = coll.delete_many( { "serial": serial } )

        logging.debug("[{0}] sensor readings have been deleted from " 
                      "MongoDB database".format(result.deleted_count))

        db.client.close()

        logging.debug("Disconnected from MongoDB")

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

        mongodb_name = ini_config.get("MongoDB", "MONGO_DB")
        db = _SensorMongoDB._get_mongodb(mongodb_name)

        coll = db['readings']

        logging.debug("Retrieving readings for sensor with serial [{0}] "
                       "between [{1}] and [{2}] from MongoDB database."
                      .format(serial, past_datetime, current_datetime))

        cursor = coll.find({ "serial": serial, 
                             "utc": { "$lt": current_datetime },
                             "utc": { "$gt": past_datetime }
                           }).sort("utc", pymongo.ASCENDING)

        data = None

        if (cursor.count() > 0):
            data = list(cursor)

        logging.debug("Readings [{0}] retrieved from MongoDB for sensor with " 
                      "serial [{1}]".format(data, serial))

        db.client.close()

        logging.debug("Disconnected from MongoDB")

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

        mongodb_name = ini_config.get("MongoDB", "MONGO_DB")
        db = _SensorMongoDB._get_mongodb(mongodb_name)

        coll = db['sensors']

        logging.debug("Adding following sensor to MongoDB database: "
                      "serial [{0}], state [{1}], name [{2}], type [{3}]"
                      .format(serial, state, name, sensor_type))

        result = coll.insert_one({"_id" : serial,
                                  "serial": serial,
                                  "geolocation": geolocation,
                                  "location": location,
                                  "address": address,
                                  "state": state,
                                  "name": name,
                                  "type": sensor_type,
                                  "description": description
                                })

        logging.debug("Sensor with id [{0}] has been inserted "
                      "into MongoDB database"
                      .format(result.inserted_id))

        db.client.close()

        logging.debug("Disconnected from MongoDB")

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

        mongodb_name = ini_config.get("MongoDB", "MONGO_DB")
        db = _SensorMongoDB._get_mongodb(mongodb_name)

        coll = db['sensors']

        logging.debug("Deleting sensor with serial [{0}] from MongoDB DB."
                      .format(serial))

        result = coll.delete_many({"serial": serial})

        logging.debug("[{0}] sensors have been deleted from MongoDB database"
                      .format(result.deleted_count))

        db.client.close()

        logging.debug("Disconnected from MongoDB")

        return


    @staticmethod
    def get_sensor(serial):
        """
        Returns a tuple corresponding to the sensor table in the database
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

        mongodb_name = ini_config.get("MongoDB", "MONGO_DB")
        db = _SensorMongoDB._get_mongodb(mongodb_name)

        coll = db['sensors']

        logging.debug("Retrieving sensor with serial [{0}] "
                      "from MongoDB database.".format(serial))

        cursor = coll.find({"serial": serial})

        # at most we are only allowed to have one sensor per serial
        if (cursor.count() > 1):
            db.client.close()
            raise RuntimeError(
                    "More than one sensor found in MongoDB [{0}] "
                    "for sensor serial [{1}]"
                    .format(db, serial))

        data = None
        for document in cursor:
            data = document

        logging.debug("[{0}] sensors have been retrieved from MongoDB DB"
                      .format(data))

        db.client.close()

        logging.debug("Disconnected from MongoDB")

        return data


class SensorDAO:
    """ Class API to provide sensor database API code
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

        if is_blank(unit):
            raise IllegalArgumentException("unit is required.")

        if not value:
            raise IllegalArgumentException("utc is required.")

        if not is_number(value):
            raise IllegalArgumentException("value is not a numeric value.")

        if is_blank(utc):
            raise IllegalArgumentException("utc is required.")

        if is_blank(serial):
            raise IllegalArgumentException("serial is required.")

        test_sensor = SensorDAO.get_sensor(serial)
        if test_sensor is None:
            raise IllegalArgumentException("sensor with serial [{0}] " 
                                            "is not registered in the system."
                                            .format(serial))

        if (ini_config.getboolean("SqlLite", "SQLITE_DB_ENABLE")):
            _SensorSQLite.add_reading(unit, value, utc, serial)
        elif (ini_config.getboolean("MongoDB", "MONGO_DB_ENABLE")):
            _SensorMongoDB.add_reading(unit, value, utc, serial)

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

        if is_blank(serial):
            raise IllegalArgumentException("serial is required.")

        if (ini_config.getboolean("SqlLite", "SQLITE_DB_ENABLE")):
            _SensorSQLite.del_readings(serial)
        elif (ini_config.getboolean("MongoDB", "MONGO_DB_ENABLE")):
            _SensorMongoDB.del_readings(serial)

        return


    @staticmethod
    def get_readings(serial, duration):
        """
        Returns .....

        Parameters
        ----------
        serial: str (required)
            sensor unique serial number
        duration: str (required)
            a valid DURATION_ENUM

        Returns
        -------
        dict:
            A sensor dictionary containing column names as keys, and
            corresponding values.
        """

        if is_blank(serial):
            raise IllegalArgumentException("serial is required.")

        if is_blank(duration):
            raise IllegalArgumentException("duration is required.")

        logging.debug("Retrieving readings from sensor with serial [{0}] using "
                      "duration [{1}] from database."
                      .format(serial, duration))

        arrow_utcnow = arrow.utcnow()
        logging.debug("current UTC now [{0}]".format(str(arrow_utcnow)))

        arrow_utcpast = None


        # I had to define the following variables to fix PyDev Error:
        # Undefined variable from import: name.  PyDev 
        last5Years = DURATION_ENUM.last5Years
        last1Year = DURATION_ENUM.last1Year
        last6Months = DURATION_ENUM.last6Months
        last90Days = DURATION_ENUM.last90Days
        last60Days = DURATION_ENUM.last60Days
        last30Days = DURATION_ENUM.last30Days
        last21Days = DURATION_ENUM.last21Days
        last7Days = DURATION_ENUM.last7Days
        last3Days = DURATION_ENUM.last3Days
        lastDay = DURATION_ENUM.lastDay
        last24Hours = DURATION_ENUM.last24Hours
        last12Hours = DURATION_ENUM.last12Hours
        last6Hours = DURATION_ENUM.last6Hours
        lastHour = DURATION_ENUM.lastHour

        if duration.lower().strip() == last5Years.name.lower():
            arrow_utcpast = arrow_utcnow.replace(years=-5)
        elif duration.lower().strip() == last1Year.name.lower():
            arrow_utcpast = arrow_utcnow.replace(years=-1)
        elif duration.lower().strip() == last6Months.name.lower():
            arrow_utcpast = arrow_utcnow.replace(months=-6)
        elif duration.lower().strip() == last90Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-90)
        elif duration.lower().strip() == last60Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-60)
        elif duration.lower().strip() == last30Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-30)
        elif duration.lower().strip() == last21Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-21)
        elif duration.lower().strip() == last7Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-7)
        elif duration.lower().strip() == last3Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-3)
        elif duration.lower().strip() == lastDay.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-1)
        elif duration.lower().strip() == last24Hours.name.lower():
            arrow_utcpast = arrow_utcnow.replace(hours=-24)
        elif duration.lower().strip() == last12Hours.name.lower():
            arrow_utcpast = arrow_utcnow.replace(hours=-12)
        elif duration.lower().strip() == last6Hours.name.lower():
            arrow_utcpast = arrow_utcnow.replace(hours=-6)
        elif duration.lower().strip() == lastHour.name.lower():
            arrow_utcpast = arrow_utcnow.replace(hours=-1)
        else:
            raise IllegalArgumentException("duration [{0}] is not valid"
                                           .format(duration))

        logging.debug("current UTC [{0}], past UTC [{1}], duration[{2}]"
                      .format(str(arrow_utcnow), str(arrow_utcpast), duration))

        current_datetime = str(arrow_utcnow)
        past_datetime = str(arrow_utcpast)

        if (ini_config.getboolean("SqlLite", "SQLITE_DB_ENABLE")):
            data = _SensorSQLite.get_readings(serial, current_datetime,
                                              past_datetime)
        elif (ini_config.getboolean("MongoDB", "MONGO_DB_ENABLE")):
            data = _SensorMongoDB.get_readings(serial, current_datetime, 
                                               past_datetime)

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

        if is_blank(serial):
            raise IllegalArgumentException("serial is required.")

        if is_blank(state):
            raise IllegalArgumentException("state is required.")

        if is_blank(name):
            raise IllegalArgumentException("name is required.")

        if is_blank(sensor_type):
            raise IllegalArgumentException("sensor_type is required.")

        test_sensor = SensorDAO.get_sensor(serial)
        if test_sensor is not None:
            raise IllegalArgumentException("sensor with serial [{0}] " 
                                            "is already registered."
                                            .format(serial))

        if (ini_config.getboolean("SqlLite", "SQLITE_DB_ENABLE")):
            _SensorSQLite.add_sensor(serial, geolocation,
                                     location, address, state,
                                     name, sensor_type, description)
        elif (ini_config.getboolean("MongoDB", "MONGO_DB_ENABLE")):
            _SensorMongoDB.add_sensor(serial, geolocation, location, 
                                      address, state, name, sensor_type, 
                                      description)

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

        if is_blank(serial):
            raise IllegalArgumentException("serial is required.")

        if (ini_config.getboolean("SqlLite", "SQLITE_DB_ENABLE")):
            _SensorSQLite.del_sensor(serial)
        elif (ini_config.getboolean("MongoDB", "MONGO_DB_ENABLE")):
            _SensorMongoDB.del_sensor(serial)

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

        if is_blank(serial):
            raise IllegalArgumentException("serial is required.")

        if (ini_config.getboolean("SqlLite", "SQLITE_DB_ENABLE")):
            data = _SensorSQLite.get_sensor(serial)
        elif (ini_config.getboolean("MongoDB", "MONGO_DB_ENABLE")):
            data = _SensorMongoDB.get_sensor(serial)

        return data


