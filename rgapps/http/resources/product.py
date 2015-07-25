"""rgapps.http.resources.product module

REST API Resource code containing information about this software.
"""
from collections import OrderedDict
import logging

from flask import jsonify
from flask.ext.restful import Resource
import pkg_resources

from rgapps.constants import NAME_KEY, VERSION_KEY, STATUS_KEY, STATUS_SUCCESS, \
    PRODUCT_KEY


__project__ = 'flaskapis'
__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["ProductInformation"]




class ProductInformation( Resource ):
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
        dist = pkg_resources.get_distribution( __project__ )

        product = OrderedDict()
        product[NAME_KEY] = dist.project_name
        product[VERSION_KEY] = dist.version
        product["author"] = __author__

        response = OrderedDict()
        response[STATUS_KEY] = STATUS_SUCCESS
        response[PRODUCT_KEY] = product

        logging.debug( "Generating information about the software product [{0}]"
                      .format( product ) )

        ordered_response = jsonify( response )

        return ordered_response
