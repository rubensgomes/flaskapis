"""rgapps.domain.product module

This module defines Product related functionality.
"""
import arrow
import pkg_resources

from rgapps.config import ini_config
from rgapps.utils.constants import PROJECT_NAME


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["Product"]



class Product:
    """ A class placeholder for product related information
    """

    Product.is_testing = ini_config.getboolean( "Flask", "TESTING" )

    def __init__( self ):
        Product.author = __author__
        if ( Product.is_testing ):
            Product.project_name = PROJECT_NAME
            Product.version = "TESTING Version"
            Product.date = str( arrow.utcnow() )
        else:
            dist = pkg_resources.get_distribution( PROJECT_NAME )
            Product.project_name = dist.project_name
            Product.version = dist.version
            Product.date = "TODO"

    def get_project_name( self ):
        # return the project name
        return Product.project_name

    def get_version( self ):
        # return the project current version
        return Product.version

    def get_date( self ):
        # return the project current version
        return Product.date

    def get_author( self ):
        # return the project author
        return Product.author
