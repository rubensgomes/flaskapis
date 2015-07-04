"""flaskapis.mqtt module

A placeholder to have code to publish IoT MQTT messages to a message broker.

THIS CODE IS STILL UNDER DEVELOPMENT / TESTING.
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

write_to_file("mqtt is now creating a Flask app...", environ['wsgi.errors'])
write_to_file("FLASKAPIS_INSTANCE_PATH [{0}]"
              .format(FLASKAPIS_INSTANCE_PATH), environ['wsgi.errors'])

# app: Flask application object
app = Flask(__name__,
            instance_path=FLASKAPIS_INSTANCE_PATH,
            instance_relative_config=True)

app.config.from_pyfile('application.cfg', silent=False)

with app.app_context():

    msg = "mqtt is now importing flaskapis.config set_up_environment ..."
    if app.config['DEBUG']:
        write_to_file(msg, environ['wsgi.errors'])
    app.logger.debug(msg)
    from flaskapis.config import set_up_environment

    msg = "mqtt is now running flaskapis.config set_up_environment ..."
    write_to_file(msg, environ['wsgi.errors'])
    app.logger.info(msg)
    set_up_environment()

    from flaskapis.mqtt.mqtt import MQTTPublisher
    msg = "mqtt is now publishing temperature ..."
    if app.config['DEBUG']:
        write_to_file(msg, environ['wsgi.errors'])
    app.logger.debug(msg)
    publisher = MQTTPublisher()
    publisher.publish_temperature(app.config['SENSOR_TEMPERATURE_SERIAL'])


if __name__ == '__main__':
    pass
