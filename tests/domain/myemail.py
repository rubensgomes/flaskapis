"""rgapps.tests.domain.myemail module

Unit test for rgapps.domain.myemail module
"""
import logging
import os
import unittest

from rgapps.config import ini_config
from rgapps.domain.myemail import EMail


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

class MyEmailTestCase(unittest.TestCase):

    LOG_FILE_PATH = ini_config.get("Logging","LOG_FILE")

    def setUp(self):
        return

    def tearDown(self):
        handlers = logging.getLogger().handlers[:]
        for handler in handlers:
            handler.close()
            logging.getLogger().removeHandler(handler)
        if os.path.isfile(MyEmailTestCase.LOG_FILE_PATH):
            os.remove(MyEmailTestCase.LOG_FILE_PATH)
        return

    def test_send_email(self):
        logging.debug("testing email send_email")
        EMail.send_email("rubens_gomes@hotmail.com",
                          "TESTING subject",
                          "TESTING message")
        return

