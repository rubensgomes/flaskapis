"""rgapps.tests.domain.sms module

Unit test for rgapps.domain.sms module
"""
import logging
import os
import unittest

from rgapps.config import ini_config
from rgapps.domain.sms import SMS


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

class SMSTestCase(unittest.TestCase):

    LOG_FILE_PATH = ini_config.get("Logging","LOG_FILE")

    def setUp(self):
        return

    def tearDown(self):
        handlers = logging.getLogger().handlers[:]
        for handler in handlers:
            handler.close()
            logging.getLogger().removeHandler(handler)
        if os.path.isfile(SMSTestCase.LOG_FILE_PATH):
            os.remove(SMSTestCase.LOG_FILE_PATH)

    def test_send_text(self):
        logging.debug("testing sms send_text")
        phone = ini_config.get("SMS", "TESTING_PHONE")
        SMS.send_text(phone, "TESTING message")
        return

