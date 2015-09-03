"""rgapps.tests.dao.sensordao module

Unit test for rgapps.dao.sensordao module
"""
import logging
import os
import unittest
from datetime import datetime

from rgapps.config.config import initialize_environment
from rgapps.dao.sensordao import SensorDAO


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

LOG_FILE_PATH = r"C:\personal\flaskapis\testing.log"
INI_FILE = r"C:\projects_GIT\flaskapis\devsettings.ini"
SERIAL = "TESTING"

class DaoTestCase( unittest.TestCase ):

    def setUp( self ):
        initialize_environment( INI_FILE,
                                log_file_path=LOG_FILE_PATH )
        DaoTestCase.sensor_db = SensorDAO()
        utc = str( datetime.utcnow() )
        logging.debug( "adding testing semsor to DB" )
        DaoTestCase.sensor_db.add_sensor(SERIAL, 
                                         "51.5033630,-0.1276250",
                                         "BASEMENT",
                                         "4102 Drew Hill Lane, Chapel Hill, NC - USA",
                                         "UP",
                                         "TESTING_SENSOR",
                                         "TEMPERATURE",
                                         "For testing purposes only")
        logging.debug( "adding testing measurement to DB" )
        DaoTestCase.sensor_db.add_measurement( "Celsius", 
                                               10, 
                                               utc, 
                                               SERIAL )
        return

    def tearDown( self ):
        logging.debug( "deleting all testing measurements from DB" )
        DaoTestCase.sensor_db.del_measurements( SERIAL )
        logging.debug( "deleting sensor from DB" )
        DaoTestCase.sensor_db.del_sensor( SERIAL )
        handlers = logging.getLogger().handlers[:]
        for handler in handlers:
            handler.close()
            logging.getLogger().removeHandler( handler )
        if os.path.isfile( LOG_FILE_PATH ):
            os.remove( LOG_FILE_PATH )

    def test_get_sensor( self ):
        logging.debug( "testing sensor add_measurement" )
        info = DaoTestCase.sensor_db.get_sensor( SERIAL )
        self.assertIsNotNone( info )
        return

    def test_get_measurements( self ):
        logging.debug( "testing sensor get_measurements" )
        readings = DaoTestCase.sensor_db.get_measurements( SERIAL,
                                                           "last3Days" )
        self.assertIsNotNone( readings )
        return
