"""flaskapis test suite

UNDER DEVELOPMENT !!!
"""


import unittest

from config.config import ConfigTestCase
from dao.sensordao import DaoTestCase
from domain.ds18b20sensor import DS18B20SensorTestCase
from domain.myemail import MyEmailTestCase
from domain.sensor import SensorTestCase
from domain.sms import SMSTestCase
from domain.units.length import LengthUnitTestCase
from domain.units.temperature import TemperatureUnitTestCase
from domain.units.weight import WeightUnitTestCase
from utils.enums import EnumsTestCase


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