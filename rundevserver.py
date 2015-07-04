"""Local runserver start-up file

This file is used to start the flaskapis server in the development
environment.  In the development environment the application runs
at localhost port 8080 as seen below.
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"


import sys

from flask import Flask

from flaskapis.constants import FLASKAPIS_INSTANCE_PATH

PORT = 8080

if __name__ == '__main__':

    try:
        # app: Flask application object
        app = Flask(__name__,
                    instance_path=FLASKAPIS_INSTANCE_PATH,
                    instance_relative_config=True)

        app.config.from_pyfile('application.cfg', silent=True)

        with app.app_context():
            from flaskapis.config import set_up_environment
            set_up_environment()

            app.logger.info("Environment has been checked okay.")
            app.logger.info("Defining the application routing.")

            from flaskapis.http import routes
            app.logger.info("Starting flaskapis at localhost port [{0}]"
                            .format(PORT))

        app.run(host="localhost",
                port=PORT,
                debug=True,
                use_reloader=True)

    except (IOError, EnvironmentError) as err:
        sys.stderr.write(str(err))
        if app.logger:
            app.logger.exception(err)
        exit(err.errno)

    except (Exception) as err:
        sys.stderr.write(str(err))
        if app.logger:
            app.logger.exception(err)
        exit(1)

    # TODO: how to stop server gracefully
    if app.logger:
        app.logger.info("Application ended with no errors.")

    exit(0)
