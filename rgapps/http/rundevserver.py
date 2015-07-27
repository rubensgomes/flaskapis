"""Flask HTTP local app start-up file

This file is used to start the flaskapis server in the development
environment.  In the development environment the application runs
at localhost port <defined in devsettings.ini> as seen below.
"""
import logging
import sys

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


def main():
    # the main funcion
    print( "initializing the environment..." )
    initialize_environment()

    try:

        instance_path = ini_config.get( "Flask", "INSTANCE_PATH" )

        # app: Flask application object
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

            logging.info( "Defining the application routing." )
            setup_routes()

            logging.info( "Setting up the Flask functions." )
            import rgapps.http.flaskfunctions

            port = ini_config.getint( "Flask", "PORT" )

            logging.info( "Starting flaskapis at localhost port [{0}]"
                          .format( port ) )

            app.run( host="localhost",
                     port=port,
                     debug=is_debug,
                     use_reloader=True )

    except ( Exception ) as err:
        sys.stderr.write( str( err ) )
        logging.exception( err )
        if ( err.errno ):
            exit( err.errno )
        else:
            exit( 1 )

    return

# run main function
main()
