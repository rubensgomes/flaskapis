"""rgapps.mqtt module

A placeholder to have code to publish MQTT messages to a message broker.
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["mqtt_publish_temperature"]

def mqtt_publish_temperature():
    """ To publish temperature sensor readings.
    """

    msg = "mqtt is now publishing the sensor temperature ..."
    logging.debug(msg)
    publisher = MQTTPublisher()
    publisher.publish_temperature(app.config['SENSOR_TEMPERATURE_SERIAL'])


if __name__ == '__main__':
    pass
