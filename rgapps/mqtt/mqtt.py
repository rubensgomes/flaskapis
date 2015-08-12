"""rgapps.mqtt.mqtt module

MQTT protocol code to publish/subscribe sensor reading messages from an
IoT sensor.
"""
from collections import OrderedDict
import json
import logging

from paho.mqtt import publish

import paho.mqtt.client as mqtt
from rgapps.config import ini_config
from rgapps.domain.ds18b20sensor import DS18B20Sensor
from rgapps.utils.exception import IllegalArgumentException
from rgapps.utils.utility import is_blank


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["MQTTPublisher"]


class MQTTSubscriber():
    """MQTT message subscriber.
    """

    # The callback for when the client receives a CONNACK response from
    # the server.

    @staticmethod
    def subscribe_temperature():
        """
        Subscribe to temperature sensor data.

        Parameters
        ----------

        Returns
        -------

        """

        # The callback for when the client receives a CONNACK response from
        # the server.
        def on_connect( client, userdata, flags, rc ):
            print( "Connected with result code " + str( rc ) )

            topic = ini_config.get( "MQTT", "MQTT_TOPIC" )

            # Subscribing in on_connect() means that if we lose the connection
            # and reconnect then subscriptions will be renewed.
            mqttc.subscribe( topic, qos=0 )

        # The callback for when a PUBLISH message is received from the server.
        def on_message( client, userdata, msg ):
            print( msg.topic + " " + str( msg.payload ) )

        mqtt_id = ini_config.get( "MQTT", "MQTT_CLIENT_ID" )
        user = ini_config.get( "MQTT", "MQTT_USERNAME" )
        pw = ini_config.get( "MQTT", "MQTT_PASSWORD" )
        host = ini_config.get( "MQTT", "MQTT_HOST" )
        port = ini_config.getint( "MQTT", "MQTT_PORT" )

        mqttc = mqtt.Client( client_id=mqtt_id,
                             clean_session=True,
                             protocol=mqtt.MQTTv31 )

        mqttc.on_connect = on_connect
        mqttc.on_message = on_message
        mqttc.username_pw_set( user, password=pw )

        logging.debug( "Connecting to MQTT Broker: "
                      "host [{0}], port [{1}], user [{2}]"
                      .format( host, port, user ) )

        mqttc.connect( host, port )

        # Blocking call that processes network traffic, dispatches callbacks
        # and handles reconnecting.
        # Other loop*() functions are available that give a threaded interface
        # and a manual interface.
        mqttc.loop_forever()

        return




class MQTTPublisher():
    """MQTT message publisher.
    """

    @staticmethod
    def publish_temperature( serial ):
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
        if is_blank( serial ):
            raise IllegalArgumentException( "serial is required" )

        mqtt_id = ini_config.get( "MQTT", "MQTT_CLIENT_ID" )
        user = ini_config.get( "MQTT", "MQTT_USERNAME" )
        pw = ini_config.get( "MQTT", "MQTT_PASSWORD" )
        host = ini_config.get( "MQTT", "MQTT_HOST" )
        port = ini_config.getint( "MQTT", "MQTT_PORT" )
        topic = ini_config.get( "MQTT", "MQTT_TOPIC" )


        mqttc = mqtt.Client( client_id=mqtt_id,
                             clean_session=True,
                             protocol=mqtt.MQTTv31 )
        mqttc.username_pw_set( user, password=pw )

        sensor_temperature = DS18B20Sensor( serial )
        readings = sensor_temperature.get_measurement()

        message = OrderedDict()
        message["value"] = readings.get_value()
        message["unit"] = readings.get_unit()
        message["utc"] = readings.get_utc()

        json_message = json.dumps( message, indent=2, sort_keys=True )

        auth = OrderedDict()
        auth["username"] = user
        auth["password"] = pw

        logging.debug( "Publishing to MQTT Broker: "
                      "host [{0}], port [{1}], client id [{2}], "
                      "user [{3}], sensor serial [{4}]"
                      .format( host, port, mqtt_id, user, serial ) )

        publish.single( topic,
                        payload=json_message, qos=0,
                        retain=False,
                        hostname=host,
                        port=port,
                        client_id=mqtt_id,
                        keepalive=20,
                        auth=auth )

        logging.debug( "Message [{0}] was published correctly: "
                      "host [{1}], port [{2}], client id [{3}], "
                      "user [{4}], sensor serial [{5}]"
                      .format( message, host, port, mqtt_id, user, serial ) )

        return

