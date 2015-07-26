"""test.rgapps.domain.ds18b20sensor module

Unit test for rgapps.domain.ds18b20sensor module
"""
import logging
import os
import unittest

from rgapps.config.config import initialize_environment
from rgapps.domain.ds18b20sensor import DS18B20Sensor


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

LOG_FILE_PATH = r"C:\personal\flaskapis\testing.log"

class ConfigTestCase( unittest.TestCase ):

    def setUp( self ):
        initialize_environment( log_file_path=LOG_FILE_PATH )
        ConfigTestCase.sensor = DS18B20Sensor( "testing" )
        return

    def tearDown( self ):
        handlers = logging.getLogger().handlers[:]
        for handler in handlers:
            handler.close()
            logging.getLogger().removeHandler( handler )
        if os.path.isfile( LOG_FILE_PATH ):
            os.remove( LOG_FILE_PATH )
        return

    def test_ds18b20sensor( self ):
        logging.debug( "testing ds18b20sensor" )
        serial = ConfigTestCase.sensor.get_serial()
        self.assertIsNotNone( serial )
        reading = ConfigTestCase.sensor.get_measurement()
        self.assertIsNotNone( reading )
        return

