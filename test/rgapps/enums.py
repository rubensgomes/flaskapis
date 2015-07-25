"""test.rgapps.enums module

Unit test for rgapps.enums module
"""
import unittest

from rgapps.enums import TEMPERATURE_ENUM, DURATION_ENUM
from rgapps.utils.exception import IllegalArgumentException


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"


class ConfigTestCase( unittest.TestCase ):

    def setUp( self ):
        return

    def tearDown( self ):
        return

    def test_temperature_enum( self ):
        unit = TEMPERATURE_ENUM.unit_name( "degC" )
        self.assertEqual( unit.upper(), "CELSIUS" )
        self.assertRaises( IllegalArgumentException,
                          TEMPERATURE_ENUM.unit_name,
                          "vasco" )
        return

    def test_duration_enum( self ):
        status = DURATION_ENUM.is_valid( "vasco" )
        self.assertFalse( status )
        return



