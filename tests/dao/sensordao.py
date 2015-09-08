"""rgapps.tests.dao.sensordao module

Unit test for rgapps.dao.sensordao module
"""
from datetime import datetime
import logging
import os
import unittest

from rgapps.config import ini_config
from rgapps.dao.sensordao import SensorDAO


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

SERIAL = "TESTING"


class DaoTestCase(unittest.TestCase):

    LOG_FILE_PATH = ini_config.get("Logging","LOG_FILE")

    def setUp(self):
        DaoTestCase.sensor_db = SensorDAO()
        utc = str(datetime.utcnow())
        logging.debug("adding testing semsor to DB")
        DaoTestCase.sensor_db.add_sensor(SERIAL,
                                         "51.5033630,-0.1276250",
                                         "BASEMENT",
                                         "4102 Drew Hill Lane, Chapel Hill, NC - USA",
                                         "UP",
                                         "TESTING_SENSOR",
                                         "TEMPERATURE",
                                         "For testing purposes only")
        logging.debug("adding testing measurement to DB")
        DaoTestCase.sensor_db.add_reading("Celsius", 10, utc, SERIAL)
        DaoTestCase.sensor_db.add_reading("Celsius", 20, utc, SERIAL)
        DaoTestCase.sensor_db.add_reading("Celsius", 30, utc, SERIAL)
        DaoTestCase.sensor_db.add_reading("Celsius", 40, utc, SERIAL)
        return

    def tearDown(self):
        logging.debug("deleting all testing measurements from DB")
        DaoTestCase.sensor_db.del_readings(SERIAL)
        logging.debug("deleting sensor from DB")
        DaoTestCase.sensor_db.del_sensor(SERIAL)
        handlers = logging.getLogger().handlers[:]
        for handler in handlers:
            handler.close()
            logging.getLogger().removeHandler(handler)
        if os.path.isfile(DaoTestCase.LOG_FILE_PATH):
            os.remove(DaoTestCase.LOG_FILE_PATH)

    def test_get_sensor(self):
        logging.debug("testing sensor add_reading")
        info = DaoTestCase.sensor_db.get_sensor(SERIAL)
        self.assertIsNotNone(info)
        return

    def test_get_readings(self):
        logging.debug("testing sensor get_readings")
        readings = DaoTestCase.sensor_db.get_readings(SERIAL, "last3Days")
        self.assertIsNotNone(readings)
        return
