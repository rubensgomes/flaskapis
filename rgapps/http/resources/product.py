"""rgapps.http.resources.product module

REST API Resource code containing information about this software.
"""
from collections import OrderedDict
import logging

from flask import jsonify
from flask_restful import Resource
import pkg_resources

from rgapps.config import ini_config
from rgapps.utils.constants import NAME_KEY, VERSION_KEY, STATUS_KEY, \
    STATUS_SUCCESS, PRODUCT_KEY


__project__ = 'flaskapis'
__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["RESTProductInfoResource"]


class RESTProductInfoResource( Resource ):
    """REST API Resource to retrieve general information about the software.
    """

    def get( self ):
        """REST GET implementation for the URI:

        http://<server>:<port>/information/product

        Parameters
        ----------

        Raises:
        ------
        """
        is_testing = ini_config.getboolean( "Flask", "TESTING" )
        project_name = None
        version = None

        if is_testing:
            project_name = "RGapps"
            version = "TESTING Version"
        else:
            dist = pkg_resources.get_distribution( __project__ )
            project_name = dist.project_name
            version = dist.version

        product = OrderedDict()
        product[NAME_KEY] = project_name
        product[VERSION_KEY] = version
        product["author"] = __author__

        response = OrderedDict()
        response[STATUS_KEY] = STATUS_SUCCESS
        response[PRODUCT_KEY] = product

        logging.debug( "Generating information about the software product [{0}]"
                      .format( product ) )

        ordered_response = jsonify( response )

        return ordered_response
