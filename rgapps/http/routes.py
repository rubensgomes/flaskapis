"""rgapps.http.routes module

This module defines the HTTP RESTFul API routes and any HTTP filters.
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

import logging

from flask import current_app, request, g
from werkzeug.exceptions import NotAcceptable, MethodNotAllowed

from rgapps.http.errors import FlaskRESTfulAPI
from rgapps.config import ini_config


# The Flask RESTful API object
api = FlaskRESTfulAPI(current_app)

# rest_apis: REST APIs that should be enabled.
rest_api_list = ini_config.get("REST", "RESTFUL_APIS").upper().split(",")
rest_apis = [str(value).strip() for value in rest_api_list]

# Temperature API
if "TEMPERATURE" in rest_apis:
    from flaskapis.resources.units.temperature import Temperature
    api.add_resource(Temperature,
                     '/temperature/<string:to_unit>')
    logging.info("temperature REST API is enabled")

# Weight API
if "WEIGHT" in rest_apis:
    from flaskapis.resources.units.weight import Weight
    api.add_resource(Weight,
                     '/weight/<string:to_unit>')
    logging.info("weight REST API is enabled")

# Length API
if "LENGTH" in rest_apis:
    from flaskapis.resources.units.length import Length
    api.add_resource(Length,
                     '/length/<string:to_unit>')
    logging.info("length REST API is enabled")

# PRODUCT_INFO
if "PRODUCT_INFO" in rest_apis:
    from flaskapis.resources.product import ProductInformation
    api.add_resource(ProductInformation,
                     '/information/product')
    logging.info("Product Info REST API is enabled")

# IoT - Sensor Temperature API
if "SENSOR_TEMPERATURE" in rest_apis:
    from flaskapis.resources.sensors.sensor import SensorTemperature
    api.add_resource(SensorTemperature,
                     '/temperature/sensors/<string:serial>')
    logging.info("Sensor Temperature REST API is enabled")

# IoT - Sensor Information API
if "SENSOR_INFO" in rest_apis:
    from flaskapis.resources.sensors.sensor import SensorInformation
    api.add_resource(SensorInformation,
                     '/information/sensors/<string:serial>')
    logging.info("Sensor Information REST API is enabled")

# IoT - Sensor Temperature Analytics API
if "SENSOR_TEMPERATURE_ANALYTICS" in rest_apis:
    from flaskapis.resources.sensors.sensor import SensorTemperatureAnalytics
    api.add_resource(SensorTemperatureAnalytics,
                     '/analytics/temperature/sensors/<string:serial>')
    logging.info("Sensor Temperature Analytics REST API is enabled")

# URL API
if "URL" in rest_apis:
    from flaskapis.resources.urls.url import URLResource
    api.add_resource(URLResource,
                     '/resource')
    logging.info("URL REST API is enabled")

@current_app.before_request
def before_request():
    """
    Handler to be run at the beginning of every single request to
    ensure that the income request is compliant to the existing
    REST API.  For example, it checks to ensure that the ACCEPT
    HTTP Header contains the Content Type support by the REST API.
    """
    url = request.url
    logging.debug("Requested URL [{0}]".format(url))

    accept = request.headers.get('Accept')
    logging.debug("HTTP Request Header Accept [{0}]".format(accept))

    accept_language = request.headers.get('Accept-Language')
    logging.debug("HTTP Request Header Accept-Language [{0}]"
                             .format(accept_language))

    content_length = request.headers.get('Content-Length')
    logging.debug("HTTP Request Content-Length [{0}]"
                             .format(content_length))

    ip = request.remote_addr
    logging.debug("Client IP Address [{0}]".format(ip))

    user_agent = request.headers.get('User-Agent')
    logging.debug("HTTP Client User-Agent [{0}]"
                             .format(user_agent))

    date = request.headers.get("Date")
    logging.debug("HTTP Request date [{0}]".format(date))

    json_weigth = request.accept_mimetypes["application/json"]
    logging.debug("application/json accept weight [{0}]"
                             .format(json_weigth))

    if json_weigth <= 0:
        # The incoming HTTP Accept header specifies a media type that is
        # not supported by this application REST API.  Currently, only
        # the JSON media type is accepted.
        msg = "HTTP Request Header Accept [{0}] not supported".format(accept)
        logging.warn(msg)
        raise NotAcceptable(msg)

    method = request.method

    if method != 'GET':
        # At this time only 'GET' methods are accepted
        msg = "HTTP Method [{0}] not supported".format(accept)
        logging.warn(msg)
        raise MethodNotAllowed(msg)

    # acquire DB connection only if DB is enabled
    if ini_config.get("SqlLite", "SQLITE_DB_ENABLE"):
        db = getattr(g, 'db', None)
        if db is None:
            import sqlite3
            g.db = sqlite3.connect(current_app.config['SQLITE_DB'])
            logging.debug("Connected to DB [{0}]".format(
               ini_config.get("SqlLite", "SQLITE_DB"))

    return

@current_app.after_request
def after_request(response):

    # log the response for debugging purposes
    logging.debug(("--------->>>RESPONSE<<<---------------\n"
                             "status [{0}]\n"
                             "charset [{1}]\n"
                             "content_length [{2}]\n"
                             "content_type [{3}]\n"
                             "mimetye [{4}]\n"
                             "data [{5}]\n")
                             .format(response.status,
                                     response.charset,
                                     response.content_length,
                                     response.content_type,
                                     response.mimetype,
                                     response.data,
                                     ))

    return response


@current_app.teardown_request
def teardown_request(exception):

    # disconnect DB connection only if DB is enabled
    if ini_config.get("SqlLite", "SQLITE_DB_ENABLE") and hasattr(g, 'db'):
        g.db.close()
        logging.debug("Disconnected from DB [{0}]".format(
            ini_config.get("SqlLite", "SQLITE_DB")))

    return

if __name__ == '__main__':
    pass
