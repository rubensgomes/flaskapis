"""rgapps.utils.exception module

This module contains exception types.
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["Error", "IllegalArgumentException", "ConfigurationException",
           "SensorReadingException"]


class Error( Exception ):
    """Base class for exceptions in this module."""
    pass


class SensorReadingException( Error ):
    """Exception raised when an expected error occurs while taking a
    measurement from a sensor.

    Attributes:
        msg  -- explanation of the error
    """

    def __init__( self, msg ):
        self.msg = msg


class IllegalArgumentException ( Error ):
    """Exception raised when an expected function argument is missing or when
    the argument has an invalid value.

    Attributes:
        msg  -- explanation of the error
    """

    def __init__( self, msg ):
        self.msg = msg


class ConfigurationException ( Error ):
    """Exception raised when a property is missing or is invalid in the
    configuration file.

    Attributes:
        msg  -- explanation of the error
    """

    def __init__( self, msg ):
        self.msg = msg


if __name__ == '__main__':
    pass