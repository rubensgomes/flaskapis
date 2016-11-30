"""flaskapis test suite

Unit Testings
"""


import unittest

from tests.config.config import ConfigTestCase
from tests.dao.sensordao import DaoTestCase
from tests.domain.ds18b20sensor import DS18B20SensorTestCase
from tests.domain.myemail import MyEmailTestCase
from tests.domain.sensor import SensorTestCase
from tests.domain.sms import SMSTestCase
from tests.domain.units.length import LengthUnitTestCase
from tests.domain.units.temperature import TemperatureUnitTestCase
from tests.domain.units.weight import WeightUnitTestCase
from tests.utils.enums import EnumsTestCase


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ConfigTestCase))
    suite.addTest(unittest.makeSuite(DaoTestCase))
    suite.addTest(unittest.makeSuite(LengthUnitTestCase))
    suite.addTest(unittest.makeSuite(TemperatureUnitTestCase))
    suite.addTest(unittest.makeSuite(WeightUnitTestCase))
    suite.addTest(unittest.makeSuite(DS18B20SensorTestCase))
    suite.addTest(unittest.makeSuite(MyEmailTestCase))
    suite.addTest(unittest.makeSuite(SensorTestCase))
    suite.addTest(unittest.makeSuite(SMSTestCase))
    suite.addTest(unittest.makeSuite(EnumsTestCase))
#    suite.addTest(MQTTTestCase())
    return suite

suite = suite()
unittest.TextTestRunner().run(suite)
