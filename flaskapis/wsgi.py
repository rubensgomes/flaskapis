"""flaskapis.wsgi module

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

from flaskapis.constants import FLASKAPIS_INSTANCE_PATH
from flaskapis.utils.utility import write_to_file

sys.stdout = sys.stderr
environ = dict(os.environ.items())

if "wsgi.errors" not in environ:
    environ["wsgi.errors"] = sys.stderr

write_to_file("mod_wsgi is now creating a Flask app...", environ['wsgi.errors'])
write_to_file("FLASKAPIS_INSTANCE_PATH [{0}]"
              .format(FLASKAPIS_INSTANCE_PATH), environ['wsgi.errors'])

# app: Flask application object
app = Flask(__name__,
            instance_path=FLASKAPIS_INSTANCE_PATH,
            instance_relative_config=True)

app.config.from_pyfile('application.cfg', silent=False)

with app.app_context():

    msg = "mod_wsgi is now importing flaskapis.config set_up_environment ..."

    if app.config['DEBUG']:
        write_to_file(msg, environ['wsgi.errors'])

    app.logger.debug(msg)

    from flaskapis.config import set_up_environment

    msg = "mod_wsgi is now running flaskapis.config set_up_environment ..."
    write_to_file(msg, environ['wsgi.errors'])
    app.logger.info(msg)

    set_up_environment()

    msg = "mod_wsgi is now importing flaskapis.http routes ..."

    if app.config['DEBUG']:
        write_to_file(msg, environ['wsgi.errors'])

    app.logger.debug(msg)

    from flaskapis.http import routes

    msg = "mod_wsgi completed importing flaskapis.http routes ..."

    if app.config['DEBUG']:
        write_to_file(msg, environ['wsgi.errors'])

    app.logger.debug(msg)

    msg = "flaskapis mod_wsgi is now running ..."
    write_to_file(msg, environ['wsgi.errors'])
    app.logger.info(msg)

if __name__ == '__main__':
    pass
