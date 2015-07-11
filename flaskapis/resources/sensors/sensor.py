"""flaskapis.resources.sensors.sensor module

This is where all the sensor flask-rest Resource code is placed.
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

from collections import OrderedDict

import arrow
from flask import request, jsonify, current_app
from flask.ext.restful import Resource
from flaskapis.constants import (
    DATA_KEY, STATUS_KEY, SENSOR_KEY, STATUS_SUCCESS
    )
from flaskapis.db.sensor import SensorDb
from flaskapis.enums import (
    DURATION_ENUM, TEMPERATURE_ENUM, UNIT_TYPES_ENUM
    )
from flaskapis.resources import http_basic_authenticate
from flaskapis.utils.utility import decimal_places
from pint.unit import UnitRegistry

from w1thermsensor import (W1ThermSensor, NoSensorFoundError,
                           SensorNotReadyError, UnsupportedUnitError)
from werkzeug.exceptions import BadRequest, NotFound, ServiceUnavailable


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["SensorInformation", "SensorTemperature", "Temperature",
           "SensorTemperatureAnalytics"]


DEFAULT_TEMPERATURE_UNIT = TEMPERATURE_ENUM.degC


class SensorTemperatureAnalytics(Resource):
    """REST API Resource to retrieve historical sensor temperature readings.
    """

    def get(self, serial):
        """REST GET implementation for the URI:

        http://<server>:<port>/analytics/temperature/sensors/<string:serial>?
            duration=<duration>

        Parameters
        ----------
        serial:  str (required)
            sensor serial number

        It is assumed that this method is called within the context of an HTTP
        request.  And that the HTTP request contains query parameters
        with the request.args as containing the following:

        duration: str (required)
            A valid duration as defined by the DURATION_ENUM

        Raises:
        ------
        BadRequest if sensor with serial is not registered or if sensor is
        not enabled.
        """
        params = request.args
        if not params:
            raise BadRequest("Parameter duration=<duration> is missing")

        if not isinstance(params, dict):
            raise BadRequest("params must be an instance of dict")

        if "duration" not in params:
            raise BadRequest("Missing required duration parameter")

        duration = params.get("duration")

        is_valid = DURATION_ENUM.is_valid(duration)
        if not is_valid:
            raise BadRequest("duration=[{0}] is not valid".format(duration))

        # retrieve sensor info from DB
        sensor_db = SensorDb()
        sensor = sensor_db.get_sensor_information(serial)

        if sensor is None:
            raise NotFound("No sensor registered for serial [{0}]"
                           .format(serial))

        readings = sensor_db.get_sensor_readings(serial, duration)

        sensor_data = dict()
        sensor_data["serial"] = sensor["serial"]

        response = OrderedDict()
        response[STATUS_KEY] = STATUS_SUCCESS
        response[SENSOR_KEY] = sensor_data
        response[DATA_KEY] = readings

        ordered_response = jsonify(response)

        return ordered_response


class SensorInformation(Resource):
    """REST API Resource to retrieve general information about a specific
    sensor.
    """

    def get(self, serial):
        """REST GET implementation for the URI:

        http://<server>:<port>/information/sensors/<string:serial>

        Parameters
        ----------
        serial:  str (required)
            sensor serial number

        Raises:
        ------
        BadRequest if sensor with serial is not registered or if sensor is
        not enabled.
        """
        # retrieve sensor info from DB
        sensor_db = SensorDb()
        sensor = sensor_db.get_sensor_information(serial)

        if sensor is None:
            raise NotFound("No sensor registered for serial [{0}]"
                           .format(serial))

        data = OrderedDict()
        data["serial"] = sensor["serial"]
        data["type"] = sensor["type"]
        data["name"] = sensor["name"]
        data["state"] = sensor["state"]
        data["geolocation"] = sensor["geolocation"]
        data["address"] = sensor["address"]
        data["location"] = sensor["location"]

        response = OrderedDict()
        response[STATUS_KEY] = STATUS_SUCCESS
        response[SENSOR_KEY] = data

        ordered_response = jsonify(response)

        return ordered_response

class SensorTemperature(Resource):
    """REST API Resource to retrieve the IoT sensor temperature.

    Notice that all communication with the actual sensor device should be
    conducted over an HTTPs (SSL) secure socket using HTTP Basic
    Authentication.

    """

    method_decorators = [http_basic_authenticate]

    def get(self, serial):
        """REST GET implementation for the URI:

        http://<server>:<port>/temperature/sensors/<string:serial>

        Parameters
        ----------
        serial:  str (required)
            sensor serial number

        Raises:
        ------
        BadRequest if sensor with serial is not registered or if sensor is
        not enabled.
        """

        sensor_temperature = Temperature()
        data = sensor_temperature.get(serial)
        response = jsonify(data)
        return response


class Temperature():
    """Class to retrieve the IoT sensor temperature.
    """

    def get(self, serial):
        """GET implementation to retrieve temperature sensors.

        It returns OrderedDict data structure with the sensor serial id,
        temperature unit, value, and timestamp.

        Parameters
        ----------
        serial:  str (required)
            sensor serial number

        Raises:
        ------
        BadRequest if sensor serial is not provided.
        """
        if not serial:
            raise BadRequest("No sensor serial provided.")

        if current_app.config["TESTING"] is True:
            temperature = 100
            current_app.logger.debug("Testing temperature in [{0}] is [{1}]"
                                     .format(DEFAULT_TEMPERATURE_UNIT.name,
                                             temperature))
        else:
            current_app.logger.debug("Reading temperature from sensor [{0}]."
                                     .format(serial))
            temperature = self._get_sensor_temperature(serial)
            current_app.logger.debug("Sensor temperature in [{0}] is [{1}]"
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

        sensor_data = dict()
        sensor_data["serial"] = serial

        arrow_utcnow = arrow.utcnow()  # current UTC timestamp

        data = OrderedDict()
        data["utc"] = str(arrow_utcnow)
        data["value"] = temperature_result
        data["unit"] = TEMPERATURE_ENUM.unit_name(DEFAULT_TEMPERATURE_UNIT)

        response = OrderedDict()
        response[STATUS_KEY] = STATUS_SUCCESS
        response[SENSOR_KEY] = sensor_data
        response[DATA_KEY] = data

        return response


    def _get_sensor_temperature(self, serial):
        """ Private method used to retrieve temperature from real sensor
        """
        ds18b20Sensor = None
        current_app.logger.debug("Reading temperature from DS18B20 sensor "
                                 "with Serial [{0}]".format(serial))

        try:
            ds18b20Sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20,
                                          serial)
            current_app.logger.debug("Instantiated DS18B20 temperature sensor "
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
                from flaskapis.resources.units import convert_unit
                current_app.logger.debug("Kevin unit is not supporte by sensor "
                                         "with serial [{0}]. Using pint to "
                                         "convert [{1}] to degK"
                                         .format(serial, degF_temperature))
                temperature = convert_unit(UNIT_TYPES_ENUM.temperature,
                                           TEMPERATURE_ENUM.degF,
                                           temperature,
                                           TEMPERATURE_ENUM.degK)
            elif (DEFAULT_TEMPERATURE_UNIT == TEMPERATURE_ENUM.degF):
                temperature = ds18b20Sensor.get_temperature(
                    W1ThermSensor.DEGREES_F
                    )
            else:
                # should never get here (sanity only).
                raise Exception("Invalid [{0}]"
                                .format(DEFAULT_TEMPERATURE_UNIT))

        except NoSensorFoundError as err:
            current_app.logger.warn("Sensor with serial [{0}] not found."
                                    " Error [{1}]."
                                    .format(serial, err))
            raise NotFound("Sensor with serial [{0}] not found. "
                           "Ensure request is sent to the IoT sensor "
                           "HTTP Gateway server"
                           .format(serial))

        except SensorNotReadyError as err:
            msg = ("Sensor with serial [{0}] not ready yet. Error [{1}]."
                   " Error [{1}]."
                   .format(serial, err))
            current_app.logger.warn(msg)
            raise ServiceUnavailable(msg)

        except UnsupportedUnitError as err:
            msg = ("Sensor with serial [{0}] does not support requested unit."
                   " Error [{1}]"
                   .format(serial, err))
            current_app.logger.warn(msg)
            raise BadRequest(msg)


        return temperature
