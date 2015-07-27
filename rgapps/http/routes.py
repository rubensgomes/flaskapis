"""rgapps.http.routes module

This module defines the HTTP RESTFul API routes and any HTTP filters.
"""
import logging

from flask.globals import current_app

from rgapps.config import ini_config
from rgapps.http.errors import FlaskRESTfulAPI
from rgapps.http.resources.product import RESTProductInfoResource
from rgapps.http.resources.sensor import RESTSensorTemperatureResource, \
    RESTSensorInfoResource, RESTSensorTemperatureAnalyticsResource
from rgapps.http.resources.units.length import RESTLengthResource
from rgapps.http.resources.units.temperature import RESTTemperatureResource
from rgapps.http.resources.units.weight import RESTWeightResource
from rgapps.http.resources.url import RESTUrlResource


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"


def setup_routes():
    """Sets up the routes for the REST resources
    """
    # The Flask RESTful API object
    api = FlaskRESTfulAPI( current_app )

    # rest_apis: REST APIs that should be enabled.
    restful_apis = ini_config.get( "REST", "RESTFUL_APIS" )
    rest_api_list = restful_apis.upper().split( "," )
    rest_apis = [str( value ).strip() for value in rest_api_list]

    # Temperature API
    if "TEMPERATURE" in rest_apis:
        api.add_resource( RESTTemperatureResource,
                         '/temperature/<string:to_unit>' )
        logging.info( "temperature REST API is enabled" )

    # Weight API
    if "WEIGHT" in rest_apis:
        api.add_resource( RESTWeightResource,
                         '/weight/<string:to_unit>' )
        logging.info( "weight REST API is enabled" )

    # Length API
    if "LENGTH" in rest_apis:
        api.add_resource( RESTLengthResource,
                         '/length/<string:to_unit>' )
        logging.info( "length REST API is enabled" )

    # PRODUCT_INFO
    if "PRODUCT_INFO" in rest_apis:
        api.add_resource( RESTProductInfoResource,
                         '/information/product' )
        logging.info( "Product Info REST API is enabled" )

    # IoT - Sensor Temperature API
    if "SENSOR_TEMPERATURE" in rest_apis:
        api.add_resource( RESTSensorTemperatureResource,
                         '/temperature/sensors/<string:serial>' )
        logging.info( "Sensor Temperature REST API is enabled" )

    # IoT - Sensor Information API
    if "SENSOR_INFO" in rest_apis:
        api.add_resource( RESTSensorInfoResource,
                         '/information/sensors/<string:serial>' )
        logging.info( "Sensor Information REST API is enabled" )

    # IoT - Sensor Temperature Analytics API
    if "SENSOR_TEMPERATURE_ANALYTICS" in rest_apis:
        api.add_resource( RESTSensorTemperatureAnalyticsResource,
                         '/analytics/temperature/sensors/<string:serial>' )
        logging.info( "Sensor Temperature Analytics REST API is enabled" )

    # URL API
    if "URL" in rest_apis:
        api.add_resource( RESTUrlResource,
                         '/resource' )
        logging.info( "URL REST API is enabled" )


if __name__ == '__main__':
    pass
