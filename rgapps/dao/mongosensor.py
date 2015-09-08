"""rgapps.dao.mongosensor module

This is where all the MongoDB sensor database code is placed.
"""
import json
import logging

from bson import json_util
import pymongo

from rgapps.config import ini_config
from rgapps.dao.mongodb import MongoDB


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["MongoSensor"]

class MongoSensor:
    """ Class to provide sensor MongoDB database API code
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

        mongodb_name = ini_config.get("MongoDB", "MONGO_DB")
        db = MongoDB.database(mongodb_name)

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
        db = MongoDB.database(mongodb_name)

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
        db = MongoDB.database(mongodb_name)

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

        if data is not None:
            # convert any MongoDB ObjectId and others (ie Binary, Code, etc) 
            # to a string equivalent such as "$oid." and revert back to dict.
            data = json.loads(json_util.dumps(data))

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
        db = MongoDB.database(mongodb_name)

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
        db = MongoDB.database(mongodb_name)

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
        db = MongoDB.database(mongodb_name)

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

        if data is not None:
            # convert any MongoDB ObjectId and others (ie Binary, Code, etc) 
            # to a string equivalent such as "$oid." and revert back to dict.
            data = json.loads(json_util.dumps(data))

        return data
