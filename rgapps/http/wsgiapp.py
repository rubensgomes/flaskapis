"""rgapps.http.wsgi module

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
from rgapps.utils.utility import write_to_file


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"


def main():
    sys.stdout = sys.stderr
    environ = dict( os.environ.items() )
    if "wsgi.errors" not in environ:
        logging.info( "wsgi.errors was not found in the environ." )
        environ["wsgi.errors"] = sys.stderr

    write_to_file( "Flask WSGI app: initializing environment.",
                   environ['wsgi.errors'] )

    initialize_environment()

    # the Apache WSGI main function.
    logging.info( "starting wsgi main." )

    instance_path = ini_config.get( "Flask", "INSTANCE_PATH" )
    logging.info( "FLASKAPIS_INSTANCE_PATH [{0}]".format( instance_path ) )

    # app: Flask application object
    logging.info( "creating Flask app ..." )
    app = Flask( __name__,
                instance_path=instance_path,
                instance_relative_config=True )
    app.config.from_pyfile( INI_FILE, silent=False )

    with app.app_context():
        logging.debug( "Flask WSGI app code is now runing within app_context" )

        logging.debug( "Flask WSGI app is now importing HTTP routes ..." )
        from rgapps.http import routes
        logging.debug( "Flask WSGI app completed importing HTTP routes" )

        logging.info( "Flask WSGI app is now running ..." )


# call main function
main()
