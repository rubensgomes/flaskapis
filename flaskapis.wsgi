""" flaskapis mod-wsgi file

This file should be placed at /home/wsgi/flaskapis on the remote web server
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

"""

ATTENTION: It is not possible to pass SetEnv environment variables
defined in the HTTP configuration files to the WSGI script.  Therefore,
we *MUST* define the following environment variable here.

"""
import os
os.environ["FLASKAPIS_INI_FILE"] = "/home/wsgi/flaskapis/application.ini"

from rgapps.http.wsgiapp import app as application
