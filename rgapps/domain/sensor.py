"""rgapps.domain.sensor module

This is where all the sensor domain code is placed.
"""
import logging
import sqlite3

import arrow
from pint.unit import UnitRegistry
from w1thermsensor import (W1ThermSensor, NoSensorFoundError,
                           SensorNotReadyError, UnsupportedUnitError)

from rgapps.config import ini_config
from rgapps.domain.units import convert_unit
from rgapps.enums import TEMPERATURE_ENUM, UNIT_TYPES_ENUM, DURATION_ENUM
from rgapps.utils.utility import decimal_places, dict_factory


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["SensorDb", "SensorTemperature"]


DEFAULT_TEMPERATURE_UNIT = TEMPERATURE_ENUM.degC

class SensorDb:
    """ Class API to update sensor database tables
    """

    def add_measurement(self, unit, value, utc, serial):
        """
        Adds given measurement data to sensor database

        Parameters
        ----------
        unit:  str (required)
            degF, degC, degF.
        value:  real (required)
            a real number
        utc: str (required)
            UTC timestamp of the reading
        serial: str (required)
            sensor unique serial number

        Returns
        -------
            nothing.
        """

        logging.debug("Inserting measurement in database: "
                      "unit [{0}], value [{1}], utc [{2}], "
                      "serial [{3}]"
                      .format(unit, value, utc, serial))

        conn = sqlite3.connect(ini_config.get("SqlLite", "SQLITE_DB"))
        logging.debug("Connected to DB [{0}]"
                      .format(ini_config.get("SqlLite", "SQLITE_DB")))

        c = conn.cursor()
        c.execute("INSERT INTO readings (id, unit, value, utc, serial) "
                  "VALUES (?,?,?,?, ?)",
                  (None, unit, value, utc, serial))

        conn.commit()
        logging.debug("Measurement has been committed in database")
        conn.close()

        logging.debug("Disconnected from DB [{0}]"
                      .format(ini_config.get("SqlLite", "SQLITE_DB")))

        return


    def get_sensor_information(self, serial):
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

        logging.debug("Retrieving sensor with serial [{0}] "
                      "from database."
                      .format(serial))

        conn = sqlite3.connect(ini_config.get("SqlLite", "SQLITE_DB"))
        logging.debug("Connected to DB [{0}]"
                      .format(ini_config.get("SqlLite", "SQLITE_DB")))

        c = conn.cursor()
        c.row_factory = dict_factory
        cursor = c.execute("SELECT * FROM sensor WHERE serial = '{0}'"
                           .format(serial))
        data = cursor.fetchone()

        conn.commit()
        conn.close()

        logging.debug("Disconnected from DB [{0}]"
                      .format(ini_config.get("SqlLite", "SQLITE_DB")))

        return data


    def get_sensor_readings(self, serial, duration):
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

        logging.debug("Retrieving readings from sensor with serial [{0}] using "
                      "duration [{1}] from database."
                      .format(serial, duration))

        arrow_utcnow = arrow.utcnow()
        logging.debug("current UTC now [{0}]"
                      .format(str(arrow_utcnow)))

        arrow_utcpast = None


        if duration.lower().strip() == DURATION_ENUM.last5Years.name.lower():
            arrow_utcpast = arrow_utcnow.replace(years=-5)
        elif duration.lower().strip() == DURATION_ENUM.last1Year.name.lower():
            arrow_utcpast = arrow_utcnow.replace(years=-1)
        elif duration.lower().strip() == DURATION_ENUM.last6Months.name.lower():
            arrow_utcpast = arrow_utcnow.replace(months=-6)
        elif duration.lower().strip() == DURATION_ENUM.last90Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-90)
        elif duration.lower().strip() == DURATION_ENUM.last60Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-60)
        elif duration.lower().strip() == DURATION_ENUM.last30Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-30)
        elif duration.lower().strip() == DURATION_ENUM.last21Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-21)
        elif duration.lower().strip() == DURATION_ENUM.last7Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-7)
        elif duration.lower().strip() == DURATION_ENUM.last3Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-3)
        elif duration.lower().strip() == DURATION_ENUM.lastDay.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-1)
        elif duration.lower().strip() == DURATION_ENUM.last24Hours.name.lower():
            arrow_utcpast = arrow_utcnow.replace(hours=-24)
        elif duration.lower().strip() == DURATION_ENUM.last12Hours.name.lower():
            arrow_utcpast = arrow_utcnow.replace(hours=-12)
        elif duration.lower().strip() == DURATION_ENUM.last6Hours.name.lower():
            arrow_utcpast = arrow_utcnow.replace(hours=-6)
        elif duration.lower().strip() == DURATION_ENUM.lastHour.name.lower():
            arrow_utcpast = arrow_utcnow.replace(hours=-1)
        else:
            raise ValueError("duration [{0}] is not valid".format(duration))

        logging.debug("current UTC [{0}], past UTC [{1}], duration[{2}]"
                      .format(str(arrow_utcnow), str(arrow_utcpast), duration))

        current_datetime = str(arrow_utcnow)
        past_datetime = str(arrow_utcpast)

        sql = ("SELECT utc, unit, value FROM readings WHERE serial = '{0}' "
               "AND utc BETWEEN '{1}' AND '{2}' "
               "ORDER BY utc ASC"
               .format(serial, past_datetime, current_datetime))

        conn = sqlite3.connect(ini_config.get("SqlLite", "SQLITE_DB"))
        logging.debug("Connected to DB [{0}]"
                      .format(ini_config.get("SqlLite", "SQLITE_DB")))

        c = conn.cursor()
        c.row_factory = dict_factory
        cursor = c.execute(sql)
        data = cursor.fetchall()

        conn.commit()
        conn.close()

        logging.debug("Disconnected from DB [{0}]"
                      .format(ini_config.get("SqlLite", "SQLITE_DB")))

        return data


class SensorTemperature:
    """Class to retrieve the sensor temperature.
    """

    def measure_temperature(self, serial):
        """to retrieve temperature sensors.

        Parameters
        ----------
        serial:  str (required)
            sensor serial number

        Returns
        -------
        float:
            the temperature

        Raises:
        ------
        ValueError if sensor serial is not provided.
        Exception for some other errors.
        """

        if not serial:
            raise ValueError("No sensor serial provided.")

        if ini_config.get("Flask", "TESTING") is True:
            temperature = 100
            logging.debug("Testing temperature in [{0}] is [{1}]"
                          .format(DEFAULT_TEMPERATURE_UNIT.name, temperature))
        else:
            logging.debug("Reading temperature from sensor [{0}]."
                          .format(serial))
            temperature = self._get_sensor_temperature(serial)
            logging.debug("Sensor temperature in [{0}] is [{1}]"
                          .format(DEFAULT_TEMPERATURE_UNIT.name,
                                  temperature))

        # use pint to represent temperature
        unit_reg = UnitRegistry(autoconvert_offset_to_baseunit=True)

        temperature_qty = temperature * unit_reg(DEFAULT_TEMPERATURE_UNIT.name)

        # restrict results to 2 decimal places.
        decimals = decimal_places(temperature_qty.magnitude)
        if(decimals > 2):
            temperature_result = round(temperature_qty.magnitude, 2)
        else:
            temperature_result = temperature_qty.magnitude

        return temperature_result


    def _get_sensor_temperature(self, serial):
        """ Private method used to retrieve temperature from real sensor
        """
        ds18b20Sensor = None
        logging.debug("Reading temperature from DS18B20 sensor "
                      "with Serial [{0}]".format(serial))

        try:
            ds18b20Sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20,
                                          serial)
            logging.debug("Instantiated DS18B20 temperature sensor "
                          "with Serial [{0}]"
                          .format(serial))

            if (DEFAULT_TEMPERATURE_UNIT == TEMPERATURE_ENUM.degC):
                temperature = ds18b20Sensor.get_temperature(
                    W1ThermSensor.DEGREES_C
                    )
            elif (DEFAULT_TEMPERATURE_UNIT == TEMPERATURE_ENUM.degK):
                degF_temperature = ds18b20Sensor.get_temperature(
                    W1ThermSensor.DEGREES_F
                    )
                # sensor only supports Celsius and Fahrenheit.
                # We should therefore use pint to convert to Kelvin
                logging.debug("Kevin unit is not supporte by sensor "
                              "with serial [{0}]. Using pint to "
                              "convert [{1}] to degK"
                              .format(serial, degF_temperature))
                temperature = convert_unit(UNIT_TYPES_ENUM.temperature,
                                           TEMPERATURE_ENUM.degF,
                                           temperature,
                                           TEMPERATURE_ENUM.degK)
            elif (DEFAULT_TEMPERATURE_UNIT == TEMPERATURE_ENUM.degF):
                temperature = ds18b20Sensor.get_temperature(
                    W1ThermSensor.DEGREES_F)
            else:
                # should never get here (sanity only).
                raise Exception("Invalid [{0}]"
                                .format(DEFAULT_TEMPERATURE_UNIT))

        except NoSensorFoundError as err:
            logging.warn("Sensor with serial [{0}] not found. Error [{1}]."
                         .format(serial, err))
            raise Exception("Sensor with serial [{0}] not found. "
                           "Ensure request is sent to the IoT sensor "
                           "HTTP Gateway server"
                           .format(serial))

        except SensorNotReadyError as err:
            msg = ("Sensor with serial [{0}] not ready yet. Error [{1}]."
                   .format(serial, err))
            logging.warn(msg)
            raise Exception(msg)

        except UnsupportedUnitError as err:
            msg = ("Sensor with serial [{0}] does not support requested unit."
                   " Error [{1}]"
                   .format(serial, err))
            logging.warn(msg)
            raise Exception(msg)


        return temperature
