"""rgapps.http.flaskfunctions module

This module registers Flask functions with the Flask current_app.  This
module should only be loaded within a Flask active application context.
"""
import logging
import sqlite3

from flask import current_app, request, g
from werkzeug.exceptions import NotAcceptable, MethodNotAllowed

from rgapps.config import ini_config


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"


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
    is_sql_enabled = ini_config.getboolean("SqlLite", "SQLITE_DB_ENABLE")
    sql_db = ini_config.get("SqlLite", "SQLITE_DB")
    if is_sql_enabled :
        db = getattr(g, 'db', None)
        if db is None:
            g.db = sqlite3.connect(sql_db)
            logging.debug("Connected to DB [{0}]".format(sql_db))

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
                                     response.data))

    return response


@current_app.teardown_request
def teardown_request(exception):

    sql_enabled = ini_config.getboolean("SqlLite", "SQLITE_DB_ENABLE")
    sql_db = ini_config.get("SqlLite", "SQLITE_DB")

    # disconnect DB connection only if DB is enabled
    if sql_enabled and hasattr(g, 'db'):
        g.db.close()
        logging.debug("Disconnected from DB [{0}]".format(sql_db))

    return

if __name__ == '__main__':
    pass
