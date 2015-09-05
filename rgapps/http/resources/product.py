"""rgapps.http.resources.product module

REST API Resource code containing information about this software.
"""
from collections import OrderedDict
import logging

from flask import jsonify
from flask_restful import Resource

from rgapps.domain.product import Product
from rgapps.utils.constants import NAME_KEY, VERSION_KEY, STATUS_KEY, \
    STATUS_SUCCESS, PRODUCT_KEY, AUTHOR_KEY, DATE_KEY, COPYRIGHT_KEY, \
    CONTACT_KEY


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["RESTProductInfoResource"]


class RESTProductInfoResource(Resource):
    """REST API Resource to retrieve general information about the software.
    """

    def get(self):
        """REST GET implementation for the URI:

        http://<server>:<port>/information/product

        Parameters
        ----------

        Raises:
        ------
        """

        product = OrderedDict()
        product[CONTACT_KEY] = Product.get_contact()
        product[COPYRIGHT_KEY] = Product.get_copyright()
        product[NAME_KEY] = Product.get_project_name()
        product[VERSION_KEY] = Product.get_version()
        product[AUTHOR_KEY] = Product.get_author()
        product[DATE_KEY] = Product.get_date()

        response = OrderedDict()
        response[STATUS_KEY] = STATUS_SUCCESS
        response[PRODUCT_KEY] = product

        logging.debug("Generating information about the software product [{0}]"
                      .format(product))

        ordered_response = jsonify(response)

        return ordered_response
