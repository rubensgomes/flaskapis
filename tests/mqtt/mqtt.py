"""rgapps.tests.mqtt.mqtt module

Unit test for rgapps.mqtt.mqtt module
"""
import logging
import os
import unittest

from rgapps.config import ini_config
from rgapps.mqtt.mqtt import MQTTPublisher


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

class MQTTTestCase(unittest.TestCase):

    LOG_FILE_PATH = ini_config.get("Logging","LOG_FILE")

    def setUp(self):
        return

    def tearDown(self):
        handlers = logging.getLogger().handlers[:]
        for handler in handlers:
            handler.close()
            logging.getLogger().removeHandler(handler)
        if os.path.isfile(MQTTTestCase.LOG_FILE_PATH):
            os.remove(MQTTTestCase.LOG_FILE_PATH)
        return

    @unittest.skip("MQTT still under development")
    def test_length_convert(self):
        logging.debug("testing MQQT publisher")
        serial = ini_config.get("Sensor", "SENSOR_TEMPERATURE_SERIAL")
        MQTTPublisher.publish_temperature(serial)
        return

