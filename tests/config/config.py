"""rgapps.tests.config.config module

Unit test for rgapps.config.config module
"""
import logging
import os
import unittest

from rgapps.config import ini_config


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

class ConfigTestCase(unittest.TestCase):

    LOG_FILE_PATH = ini_config.get("Logging","LOG_FILE")

    def setUp(self):
        logging.debug("Testing ConfigTestCase...")
        return

    def tearDown(self):
        handlers = logging.getLogger().handlers[:]
        for handler in handlers:
            handler.close()
            logging.getLogger().removeHandler(handler)
        if os.path.isfile(ConfigTestCase.LOG_FILE_PATH):
            os.remove(ConfigTestCase.LOG_FILE_PATH)
        return

    def test_logging(self):
        logging.debug("Log file [{0}]"
                      .format(ConfigTestCase.LOG_FILE_PATH))
        return

