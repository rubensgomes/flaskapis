"""test.rgapps.domain.sensor module

Unit test for rgapps.domain.sensor module
"""
from datetime import datetime
import logging
import os
import unittest

from rgapps.config.config import initialize_environment
from rgapps.domain.sensor import Measurement


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
        return

    def tearDown( self ):
        handlers = logging.getLogger().handlers[:]
        for handler in handlers:
            handler.close()
            logging.getLogger().removeHandler( handler )
        if os.path.isfile( LOG_FILE_PATH ):
            os.remove( LOG_FILE_PATH )
        return

    def test_measurement( self ):
        logging.debug( "testing Measurement" )
        utc = str( datetime.utcnow() )
        reading = Measurement( 20, "Celsius", utc )
        self.assertIsNotNone( reading )
        value = reading.get_value()
        self.assertEquals( 20, value )
        unit = reading.get_unit()
        self.assertEquals( "Celsius", unit )
        reading_utc = reading.get_utc()
        self.assertEquals( utc, reading_utc )
        return

