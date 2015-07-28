"""rgapps.http.resources.url module

This is where all the URL flask-rest Resource code is placed.
"""
from collections import OrderedDict
import sys
import urllib2

from bs4 import BeautifulSoup
from flask import request, jsonify
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from rgapps.utils.constants import URL_KEY, DATA_KEY


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"


__all__ = ["RESTUrlResource"]


class RESTUrlResource( Resource ):
    """REST API Resource to retrieve the resource from given HTTP URL
    sensor.
    """

    def get( self ):
        """REST GET implementation for the URI:

        http://<server>:<port>/resource?httpurl=<string:httpurl>

        Parameters
        ----------
        httpurl:  str (required)
            the HTTP URL for the resource to retrieve

        Raises:
        ------
        BadRequest if HTTP URL is not valid
        """
        params = request.args
        if not params:
            raise BadRequest( "Parameters "
                             "httpurl=<httpurl> "
                             "is missing" )

        if "httpurl" not in params:
            raise BadRequest( "Missing required httpurl parameter" )

        url = params.get( "httpurl" )

        req = urllib2.Request( url )
        try:
            resp = urllib2.urlopen( req, timeout=5 )
        except urllib2.URLError as err:
            sys.stderr.write( str( err ) )
            raise BadRequest( ( "URL request to httpurl=[{0}] failed: [{1}] " )
                             .format( url, err ) )

        page = resp.read().strip()

        soup = BeautifulSoup( page, 'html.parser' )
        html = soup.prettify()

        data = OrderedDict()
        data[URL_KEY] = url
        data[DATA_KEY] = html

        json_response = jsonify( data )
        return json_response


if __name__ == "__main__":
    pass
