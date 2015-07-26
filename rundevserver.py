"""Local runserver start-up file

This file is used to start the flaskapis server in the development
environment.  In the development environment the application runs
at localhost port <defined in devsettings.ini> as seen below.
"""
import logging
import sys

from flask import Flask

from rgapps.config import ini_config
from rgapps.config.config import initialize_environment
from rgapps.constants import INI_FILE
from rgapps.http.routes import setup_routes


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"


port = ini_config.get( "Flask", "PORT" )
flask_instance_path = ini_config.get( "Flask", "INSTANCE_PATH" )
log_file = ini_config.get( "Logging", "LOG_FILE" )

if __name__ == '__main__':

    try:
        # app: Flask application object
        app = Flask( __name__,
                    instance_path=flask_instance_path,
                    instance_relative_config=True )

        # devsettings.cfg is local and only available in the DEV environment
        app.config.from_pyfile( INI_FILE, silent=True )

        with app.app_context():
            initialize_environment( log_path=log_file )

            logging.info( "Environment has been checked okay." )
            logging.info( "Defining the application routing." )

            setup_routes()
            logging.info( "Starting flaskapis at localhost port [{0}]"
                            .format( port ) )

        app.run( host="localhost",
                port=port,
                debug=True,
                use_reloader=True )

    except ( IOError, EnvironmentError ) as err:
        sys.stderr.write( str( err ) )
        if logging:
            logging.exception( err )
        exit( err.errno )

    except ( Exception ) as err:
        sys.stderr.write( str( err ) )
        if logging:
            logging.exception( err )
        exit( 1 )

    # TODO: how to stop server gracefully
    if logging:
        logging.info( "Application ended with no errors." )

    exit( 0 )
