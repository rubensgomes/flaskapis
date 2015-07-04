"""flaskapis.resources package

A sub-package for all the REST Resources code.

Modules:
-------
product: REST API Resource to render information about the product

Sub-Packages:
------------
sensors: a placeholder for sensors resources
units:  a placeholder for the units resources
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["product", "sensors", "units", "urls", "http_basic_authenticate"]

from functools import wraps

from flask import request, current_app
from flask.ext import restful
from werkzeug.exceptions import Unauthorized


def _basicAuthentication():
    """This is a private helper method used by the http_basic_authenticate.
    """
    auth = request.authorization
    current_app.logger.debug("Authenticating HTTP Basic Authentication "
                             "using Authorization [{0}]".format(auth))

    if "SENSOR_REST_API_USERNAME" not in current_app.config:
        raise EnvironmentError("SENSOR_REST_API_USERNAME property missing "
                               "in application.cfg")

    if "SENSOR_REST_API_PASSWORD" not in current_app.config:
        raise EnvironmentError("SENSOR_REST_API_PASSWORD property missing "
                               "in application.cfg")

    valid_username = current_app.config['SENSOR_REST_API_USERNAME']
    valid_password = current_app.config['SENSOR_REST_API_PASSWORD']

    if not auth:
        current_app.logger.debug("HTTP Basic Authentication header not found.")
        return False

    elif (auth.username != valid_username):
        current_app.logger.debug("user [{0}] is not valid.  "
                                 "Authentication failed"
                                 .format(auth.username))
        return False

    elif (auth.password != valid_password):
        current_app.logger.debug("Password is not valid. "
                                 "user [{0}] failed to be authenticated."
                                .format(auth.username))
        return False


    current_app.logger.debug("user [{0}] has been authenticated."
                             .format(auth.username))
    return True


def http_basic_authenticate(func):
    """ This is a decorator function used to replace the flask-restful
    method-decorator property inside flask-restful Resource classes.
    It authenticates the user using the HTTP Basic Authentication protocol.

    Parameters:
    ----------
    func: python function
        The function being decorated.

    Returns:
    -------
    The decorator function used in the method_decorators declared inside
    the flask-restful Resources classes.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        authenticated = _basicAuthentication()

        if authenticated:
            return func(*args, **kwargs)

        current_app.logger.info("Aborting request with 401 status code.")
        resource_url = request.base_url
        raise Unauthorized(
            "The REST resource [{0}] requires a valid username/passsord."
            .format(resource_url)
            )

    return wrapper


if __name__ == '__main__':
    pass
