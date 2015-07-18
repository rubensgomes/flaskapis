"""flaskapis.mqtt.mqtt module

MQTT protocol code to publish messages from the IoT sensor to an MQTT broker
"""
from collections import OrderedDict
import json

from flask import current_app
from paho.mqtt import publish
from paho.mqtt.client import MQTT_ERR_SUCCESS
from werkzeug.exceptions import BadRequest

from flaskapis.resources.sensors.sensor import Temperature
import paho.mqtt.client as mqtt


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["MQTTPublisher"]



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

        # test serial
        if not serial:
            raise BadRequest("serial is missing")

        mqtt_id = current_app.config['MQTT_CLIENT_ID']
        user = current_app.config['MQTT_USERNAME']
        pw = current_app.config['MQTT_PASSWORD']
        host = current_app.config['MQTT_HOST']
        port = current_app.config['MQTT_PORT']
        topic = current_app.config['MQTT_TOPIC']


        mqttc = mqtt.Client(client_id=mqtt_id, clean_session=True,
                            protocol=mqtt.MQTTv31)
        mqttc.username_pw_set(user, password=pw)

        current_app.logger.debug("Connecting to MQTT Broker: "
                                 "host [{0}], port [{1}], client id [{2}], "
                                 "user [{3}], sensor serial [{4}]"
                                 .format(host, port, mqtt_id, user, serial))

        sensor_temperature = Temperature()
        message = sensor_temperature.get(serial)
        json_message = json.dumps(message, indent=2, sort_keys=True)

        auth = OrderedDict()
        auth["username"] = user
        auth["password"] = pw

        publish.single(topic, payload=json_message, qos=0,
                       retain=False, hostname=host,
                       port=port, client_id=mqtt_id,
                       keepalive=20, auth=auth)

        current_app.logger.debug("Message was published correctly: "
                                 "host [{0}], port [{1}], client id [{2}], "
                                 "user [{3}], sensor serial [{4}]"
                                 .format(host, port, mqtt_id, user, serial))

        return

