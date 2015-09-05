"""Flask Apache WSGI start-up file

Apache WSGI Flask application

This is a placeholder to have code to kick-off the Apache2 mod_wsgi server.
"""
import logging

from flask import Flask

from rgapps.config import ini_config
from rgapps.config.config import initialize_environment
from rgapps.http.routes import setup_routes


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

INI_FILE = r"/home/wsgi/flaskapis/application.ini"

# initialize_environment MUST be called first !!!
initialize_environment(INI_FILE)

instance_path = ini_config.get("Flask", "INSTANCE_PATH")

logging.info("creating Flask app ...")
app = Flask(__name__,
            instance_path=instance_path,
            instance_relative_config=True)

is_debug = ini_config.getboolean("Flask", "DEBUG")
is_testing = ini_config.getboolean("Flask", "TESTING")
is_json_sort_keys = ini_config.getboolean("Flask", "JSON_SORT_KEYS")
max_content_length = ini_config.getint("Flask", "MAX_CONTENT_LENGTH")

app.config.update(DEBUG=is_debug,
                   TESTING=is_testing,
                   JSON_SORT_KEYS=is_json_sort_keys,
                   MAX_CONTENT_LENGTH=max_content_length)

with app.app_context():
    logging.info("Configuring the Flask HTTP routing.")
    setup_routes()

    logging.info("Setting up the Flask functions.")
    import rgapps.http.flaskfunctions

    logging.info("Flask WSGI app is now running ...")


if __name__ == '__main__':
    pass
