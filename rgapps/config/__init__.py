"""rgapps.config subpackage

This package contains configuration related code.

Modules:
-------
config: a module to place all file configuration code

Sub-Packages:
------------
"""
from six.moves import configparser


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["config", "ini_config"]


# the application INI configuration
ini_config = configparser.SafeConfigParser()

if __name__ == '__main__':
    pass
