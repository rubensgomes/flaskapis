""" flaskapis mod-wsgi file

This file should be placed at /home/wsgi/flaskapis on the remote web server
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

from rgapps.http.wsgiapp import app as application
