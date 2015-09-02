"""test.rgapps.mqtt.mqtt module

Unit test for rgapps.mqtt.mqtt module
"""
import logging
import os
import unittest

from rgapps.config import ini_config
from rgapps.config.config import initialize_environment
from rgapps.mqtt.mqtt import MQTTPublisher


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

LOG_FILE_PATH = r"C:\personal\flaskapis\testing.log"
INI_FILE = r"C:\projects_GIT\flaskapis\devsettings.ini"

class ConfigTestCase( unittest.TestCase ):

    def setUp( self ):
        initialize_environment( INI_FILE,
                                log_file_path=LOG_FILE_PATH )
        return

    def tearDown( self ):
        handlers = logging.getLogger().handlers[:]
        for handler in handlers:
            handler.close()
            logging.getLogger().removeHandler( handler )
        if os.path.isfile( LOG_FILE_PATH ):
            os.remove( LOG_FILE_PATH )
        return

    def test_length_convert( self ):
        logging.debug( "testing MQQT publisher" )
        serial = ini_config.get( "Sensor", "SENSOR_TEMPERATURE_SERIAL" )
        MQTTPublisher.publish_temperature( serial )
        return

