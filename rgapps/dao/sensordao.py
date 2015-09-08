"""rgapps.dao.sensordao module

This is where all the sensor database code is placed.
"""


import logging

import arrow

from rgapps.config import ini_config
from rgapps.utils.enums import DURATION_ENUM
from rgapps.utils.exception import IllegalArgumentException
from rgapps.utils.utility import is_blank, is_number
from rgapps.dao.mongosensor import MongoSensor
from rgapps.dao.sqlitesensor import SQLiteSensor

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["SensorDAO"]



class SensorDAO:
    """ Class API to provide sensor database API code
    """

    SENSOR_DB = None
    # Strategy design pattern along with duck typing.
    if (ini_config.getboolean("SqlLite", "SQLITE_DB_ENABLE")):
        SENSOR_DB = SQLiteSensor()
    elif (ini_config.getboolean("MongoDB", "MONGO_DB_ENABLE")):
        SENSOR_DB = MongoSensor()


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

        SensorDAO.SENSOR_DB.add_reading(unit, value, utc, serial)

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

        SensorDAO.SENSOR_DB.del_readings(serial)

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

        data = SensorDAO.SENSOR_DB.get_readings(serial, current_datetime, 
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

        SensorDAO.SENSOR_DB.add_sensor(serial, geolocation, location, address, 
                                       state, name, sensor_type, description)

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

        SensorDAO.SENSOR_DB.del_sensor(serial)

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

        data = SensorDAO.SENSOR_DB.get_sensor(serial)

        return data


