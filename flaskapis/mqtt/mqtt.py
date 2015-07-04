"""flaskapis.mqtt.mqtt module

MQTT protocol code to publish messages from the IoT sensor to an MQTT broker
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["MQTTPublisher"]

import paho.mqtt.client as mqtt

from flask import current_app
from flaskapis.resources.sensors.sensor import Temperature

class MQTTPublisher():
    """MQTT message publisher.
    """

    def publish_temperature(self, serial):
        """
        Publishes the given temperature sensor data to MQTT
        message broker.

        Parameters
        ----------
        serial:  str (required)
            sensor serial number

        Returns
        -------

        """
        mqtt_id = current_app.config['MQTT_CLIENT_ID']
        user = current_app.config['MQTT_USERNAME']
        pw = current_app.config['MQTT_PASSWORD']
        host = current_app.config['MQTT_HOST']
        port = current_app.config['MQTT_PORT']

        mqttc = mqtt.Client(client_id=mqtt_id, clean_session=False,
                            protocol=mqtt.MQTTv31)
        mqttc.username_pw_set(user, password=pw)

        current_app.logger.debug("Connecting to MQTT Broker: "
                                 "host [{0}], port [{1}], client id [{2}], "
                                 "user [{3}], sensor serial [{4}]"
                                 .format(host, port, mqtt_id, user, serial))

        mqttc.connect(host, port=port, keepalive=60)

        sensor_temperature = Temperature()
        message = sensor_temperature.get(serial)

        result = mqttc.publish("SENSOR TEMPERATURE",
                      payload=message, qos=0, retain=False)

        current_app.logger.debug("result [{0}]".format(result))

        current_app.logger.debug("Disconnecting from MQTT Broker: "
                                 "host [{0}], port [{1}], client id [{2}], "
                                 "user [{3}], sensor serial [{4}]"
                                 .format(host, port, mqtt_id, user, serial))

        mqttc.disconnet()

        return

