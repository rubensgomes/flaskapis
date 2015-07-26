"""test.rgapps.domain.email module

Unit test for rgapps.domain.email module
"""
import logging
import os
import unittest

from rgapps.config.config import initialize_environment
from rgapps.domain.myemail import EMail


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

    def test_send_email( self ):
        logging.debug( "testing email send_email" )
        EMail.send_email( "rubens_gomes@hotmail.com",
                          "TESTING subject",
                          "TESTING message" )
        return

