"""rgapps.http.resources.sensor module

This is where all the sensor flask-rest Resource code is placed.
"""
from collections import OrderedDict

from flask import request, jsonify
from flask.ext.restful import Resource
from werkzeug.exceptions import BadRequest, NotFound

from rgapps.dao.sensordao import SensorDAO
from rgapps.domain.ds18b20sensor import DS18B20Sensor
from rgapps.http import http_basic_authenticate
from rgapps.utils.constants import STATUS_KEY, STATUS_SUCCESS, SENSOR_KEY, \
    DATA_KEY
from rgapps.utils.enums import DURATION_ENUM


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["RESTSensorInfoResource", "RESTSensorTemperatureResource",
           "RESTSensorTemperatureAnalyticsResource"]


class RESTSensorTemperatureAnalyticsResource( Resource ):
    """REST API Resource to retrieve historical sensor temperature readings.
    """

    def get( self, serial ):
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
            raise BadRequest( "Parameter duration=<duration> is missing" )

        if not isinstance( params, dict ):
            raise BadRequest( "params must be an instance of dict" )

        if "duration" not in params:
            raise BadRequest( "Missing required duration parameter" )

        duration = params.get( "duration" )

        is_valid = DURATION_ENUM.is_valid( duration )
        if not is_valid:
            raise BadRequest( "duration=[{0}] is not valid".format( duration ) )

        # retrieve sensor info from DB
        sensor = SensorDAO.get_sensor_information( serial )

        if sensor is None:
            raise NotFound( "No sensor registered for serial [{0}]"
                           .format( serial ) )

        readings = SensorDAO.get_sensor_readings( serial, duration )

        sensor_data = dict()
        sensor_data["serial"] = sensor["serial"]

        response = OrderedDict()
        response[STATUS_KEY] = STATUS_SUCCESS
        response[SENSOR_KEY] = sensor_data
        response[DATA_KEY] = readings

        json_response = jsonify( response )
        return json_response


class RESTSensorInfoResource( Resource ):
    """REST API Resource to retrieve general information about a specific
    sensor.
    """

    def get( self, serial ):
        """REST GET implementation for the URI:

        http://<server>:<port>/information/sensors/<string:serial>

        Parameters
        ----------
        serial:  str (required)
            sensor serial number

        Raises:
        ------
        NotFound if sensor with serial is not found.
        """
        # retrieve sensor info from DB
        sensor = SensorDAO.get_sensor_information( serial )

        if sensor is None:
            raise NotFound( "No sensor registered for serial [{0}]"
                           .format( serial ) )

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

        json_response = jsonify( response )
        return json_response


class RESTSensorTemperatureResource( Resource ):
    """REST API Resource to retrieve the IoT sensor temperature.

    Notice that all communication with the actual sensor device should be
    conducted over an HTTPs (SSL) secure socket using HTTP Basic
    Authentication.

    """

    method_decorators = [http_basic_authenticate]

    def get( self, serial ):
        """REST GET implementation for the URI:

        http://<server>:<port>/temperature/sensors/<string:serial>

        Parameters
        ----------
        serial:  str (required)
            sensor serial number

        """
        temperature_sensor = DS18B20Sensor( serial )
        measurement = temperature_sensor.get_measurement()

        sensor_data = dict()
        sensor_data["serial"] = serial

        data = OrderedDict()
        data["utc"] = measurement.get_utc()
        data["value"] = measurement.get_value()
        data["unit"] = measurement.get_unit()

        response = OrderedDict()
        response[STATUS_KEY] = STATUS_SUCCESS
        response[SENSOR_KEY] = sensor_data
        response[DATA_KEY] = data

        json_response = jsonify( response )
        return json_response

