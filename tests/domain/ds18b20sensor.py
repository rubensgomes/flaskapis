"""rgapps.tests.domain.ds18b20sensor module

Unit test for rgapps.domain.ds18b20sensor module
"""
import logging
import os
import unittest

from rgapps.config import ini_config
from rgapps.domain.ds18b20sensor import DS18B20Sensor


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

class DS18B20SensorTestCase(unittest.TestCase):

    LOG_FILE_PATH = ini_config.get("Logging","LOG_FILE")

    def setUp(self):
        DS18B20SensorTestCase.sensor = DS18B20Sensor("testing")
        return

    def tearDown(self):
        handlers = logging.getLogger().handlers[:]
        for handler in handlers:
            handler.close()
            logging.getLogger().removeHandler(handler)
        if os.path.isfile(DS18B20SensorTestCase.LOG_FILE_PATH):
            os.remove(DS18B20SensorTestCase.LOG_FILE_PATH)
        return

    def test_ds18b20sensor(self):
        logging.debug("testing ds18b20sensor")
        serial = DS18B20SensorTestCase.sensor.get_serial()
        self.assertIsNotNone(serial)
        reading = DS18B20SensorTestCase.sensor.get_measurement()
        self.assertIsNotNone(reading)
        return

