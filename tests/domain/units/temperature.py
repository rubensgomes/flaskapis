"""rgapps.tests.domain.units.temperature module

Unit test for rgapps.domain.units.temperature module
"""
import logging
import os
import unittest

from rgapps.config import ini_config
from rgapps.domain.units.temperature import Temperature


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"


class TemperatureUnitTestCase(unittest.TestCase):

    LOG_FILE_PATH = ini_config.get("Logging","LOG_FILE")

    def setUp(self):
        return

    def tearDown(self):
        handlers = logging.getLogger().handlers[:]
        for handler in handlers:
            handler.close()
            logging.getLogger().removeHandler(handler)
        if os.path.isfile(TemperatureUnitTestCase.LOG_FILE_PATH):
            os.remove(TemperatureUnitTestCase.LOG_FILE_PATH)
        return

    def test_length_convert(self):
        logging.debug("testing temperature convert")
        result = Temperature.convert(18, "degC", "degF")
        self.assertIsNotNone(result)
        return

