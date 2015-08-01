"""rgapps.domain.product module

This module defines Product related functionality.
"""
import os
import re
import time

import pip
import pkg_resources

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
    author = __author__
    copyright = __copyright__
    contact = __email__
    dist = pkg_resources.get_distribution( PROJECT_NAME )
    project_name = dist.project_name
    version = dist.version

    date = None
    pattern = re.compile( project_name + "*", re.IGNORECASE )
    for package in pip.get_installed_distributions():
        if pattern.match( package.key ):
            date = time.ctime( os.path.getctime( package.location ) )
            break

    @staticmethod
    def get_project_name():
        # return the project name
        return Product.project_name

    @staticmethod
    def get_version():
        # return the project current version
        return Product.version

    @staticmethod
    def get_date():
        # return the project current version
        return Product.date

    @staticmethod
    def get_author():
        # return the project author
        return Product.author

    @staticmethod
    def get_copyright():
        # return the copyright
        return Product.copyright

    @staticmethod
    def get_contact():
        # return the contact information
        return Product.contact

