"""rgapps.http.wsgi module

This is a placeholder to have code to kick-off the Apache2 mod_wsgi server.
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

import os
import sys

from flask import Flask

from rgapps.constants import INI_FILE
from rgapps.config import ini_config
from rgapps.config.config import initialize_environment
from rgapps.utils.utility import write_to_file


sys.stdout = sys.stderr
environ = dict(os.environ.items())

if "wsgi.errors" not in environ:
    environ["wsgi.errors"] = sys.stderr

write_to_file("mod_wsgi is now creating a Flask app...",
              environ['wsgi.errors'])

initialize_environment()

flask_instance_path = ini_config.get("Flask", "INSTANCE_PATH")
write_to_file("FLASKAPIS_INSTANCE_PATH [{0}]".format(flask_instance_path),
              environ['wsgi.errors'])

# app: Flask application object
app = Flask(__name__,
            instance_path=flask_instance_path,
            instance_relative_config=True)
app.config.from_pyfile(INI_FILE, silent=False)

with app.app_context():

    msg = "mod_wsgi is now importing flaskapis.config set_up_environment ..."

    if app.config['DEBUG']:
        write_to_file(msg, environ['wsgi.errors'])

    app.logger.debug(msg)

    msg = "mod_wsgi is now running flaskapis.config set_up_environment ..."
    write_to_file(msg, environ['wsgi.errors'])
    app.logger.info(msg)

    msg = "mod_wsgi is now importing flaskapis.http routes ..."

    if app.config['DEBUG']:
        write_to_file(msg, environ['wsgi.errors'])

    app.logger.debug(msg)

    from rgapps.http import routes

    msg = "mod_wsgi completed importing flaskapis.http routes ..."

    if app.config['DEBUG']:
        write_to_file(msg, environ['wsgi.errors'])

    app.logger.debug(msg)

    msg = "flaskapis mod_wsgi is now running ..."
    write_to_file(msg, environ['wsgi.errors'])
    app.logger.info(msg)

if __name__ == '__main__':
    pass
