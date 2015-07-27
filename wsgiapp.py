"""Flask Apache WSGI start-up file

Apache WSGI Flask application

This is a placeholder to have code to kick-off the Apache2 mod_wsgi server.
"""
import logging
import os
import sys

from flask import Flask

from rgapps.config import ini_config
from rgapps.config.config import initialize_environment
from rgapps.constants import INI_FILE
from rgapps.http.routes import setup_routes
from rgapps.utils.utility import write_to_file


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"


sys.stdout = sys.stderr
environ = dict( os.environ.items() )
if "wsgi.errors" not in environ:
    logging.info( "wsgi.errors was not found in the environ." )
    environ["wsgi.errors"] = sys.stderr

write_to_file( "Flask WSGI app: initializing environment.",
               environ['wsgi.errors'] )
initialize_environment()


# app: Flask application object
logging.info( "creating Flask app ..." )

instance_path = ini_config.get( "Flask", "INSTANCE_PATH" )
app = Flask( __name__,
            instance_path=instance_path,
            instance_relative_config=True )

is_debug = ini_config.getboolean( "Flask", "DEBUG" )
is_testing = ini_config.getboolean( "Flask", "TESTING" )
is_json_sort_keys = ini_config.getboolean( "Flask", "JSON_SORT_KEYS" )
max_content_length = ini_config.getint( "Flask", "MAX_CONTENT_LENGTH" )

app.config.update( DEBUG=is_debug,
                   TESTING=is_testing,
                   JSON_SORT_KEYS=is_json_sort_keys,
                   MAX_CONTENT_LENGTH=max_content_length )

with app.app_context():
    logging.info( "Code is now running with Flask app context." )

    logging.info( "Configuring the application routing." )
    setup_routes()

    logging.info( "Setting up the Flask functions." )
    import rgapps.http.flaskfunctions

    logging.info( "Flask WSGI app is now running ..." )


if __name__ == '__main__':
    pass
