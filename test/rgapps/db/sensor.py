"""test.rgapps.db.sensor module

Unit test for rgapps.db.sensor module
"""
import logging
import os
import unittest
from datetime import datetime

from rgapps.config.config import initialize_environment
from rgapps.db.sensor import SensorDb


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

LOG_FILE_PATH = r"C:\personal\flaskapis\testing.log"

class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        initialize_environment(log_file_path=LOG_FILE_PATH)
        ConfigTestCase.sensor_db = SensorDb()
        return

    def tearDown(self):
        handlers = logging.getLogger().handlers[:]
        for handler in handlers:
            handler.close()
            logging.getLogger().removeHandler(handler)
        if os.path.isfile(LOG_FILE_PATH):
            os.remove(LOG_FILE_PATH)

    def test_add_measurement(self):
        logging.debug("testing sensor add_measurement")
        utc = datetime.utcnow()
        ConfigTestCase.sensor_db.add_measurement("Celsius", 10, utc, "testing")
        return

    def test_get_sensor_information(self):
        logging.debug("testing sensor add_measurement")
        info = ConfigTestCase.sensor_db.get_sensor_information("testing")
        return

    def test_get_sensor_readings(self):
        logging.debug("testing sensor get_sensor_readings")
        readings = ConfigTestCase.sensor_db.get_sensor_readings("testing",
                                                                "last3Days")
        return
