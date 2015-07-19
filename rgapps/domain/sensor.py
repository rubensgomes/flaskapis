"""rgapps.domain.sensor module

This is where all the sensor domain code is placed.
"""
import logging

from pint.unit import UnitRegistry
from w1thermsensor import (W1ThermSensor, NoSensorFoundError,
                           SensorNotReadyError, UnsupportedUnitError)

from rgapps.config import ini_config
from rgapps.domain.units import convert_unit
from rgapps.enums import TEMPERATURE_ENUM, UNIT_TYPES_ENUM
from rgapps.utils.utility import decimal_places


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["Temperature"]


DEFAULT_TEMPERATURE_UNIT = TEMPERATURE_ENUM.degC

class Temperature:
    """Class to retrieve the IoT sensor temperature.
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
