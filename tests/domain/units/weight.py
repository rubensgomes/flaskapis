"""rgapps.tests.domain.units.weight module

Unit test for rgapps.domain.units.weight module
"""
import logging
import os
import unittest

from rgapps.config import ini_config
from rgapps.domain.units.weight import Weight


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"


class WeightUnitTestCase(unittest.TestCase):

    LOG_FILE_PATH = ini_config.get("Logging","LOG_FILE")

    def setUp(self):
        return

    def tearDown(self):
        handlers = logging.getLogger().handlers[:]
        for handler in handlers:
            handler.close()
            logging.getLogger().removeHandler(handler)
        if os.path.isfile(WeightUnitTestCase.LOG_FILE_PATH):
            os.remove(WeightUnitTestCase.LOG_FILE_PATH)
        return

    def test_length_convert(self):
        logging.debug("testing weight convert")
        result = Weight.convert(184, "kg", "lb")
        self.assertIsNotNone(result)
        return

