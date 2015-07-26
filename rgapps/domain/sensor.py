"""rgapps.domain.sensor module

This module defines some abstractions used by concrete sensor objects.
"""
from abc import ABCMeta, abstractmethod

from rgapps.utils.exception import IllegalArgumentException
from rgapps.utils.utility import is_number, is_blank


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["Measurement", "Sensor"]



class Measurement:
    """An data structure to represent a device (sensor) reading measurement.
    """

    def __init__( self, value, unit, utc ):
        """constructor.

        Parameters
        ----------
        value:  float (required)
            the measurement reading numeric value
        value:  string (required)
            the measurement reading unit
        utc: string (required)
            the UTC timestamp
        """
        if not is_number( value ):
            raise IllegalArgumentException( "value is invalid." )

        if is_blank( unit ):
            raise IllegalArgumentException( "unit is required." )

        if is_blank( utc ):
            raise IllegalArgumentException( "utc is required." )

        self.value = value
        self.unit = unit
        self.utc = utc
        return

    def __str__( self ):
        # to string method.
        return str( "value [{0}], unit [{1}], utc [{2}]"
                    .format( str( self.value ), self.unit, self.utc ) )

    def get_value( self ):
        # the reading numeric float value
        return self.value

    def get_unit( self ):
        # the reading string text unit
        return self.unit

    def get_utc( self ):
        # the reading string text UTC timestamp
        return self.utc


class Sensor:
    """An abastract base class to represent a device (sensor).
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_serial( self ):
        """The sensor serial or other identification .

        Returns
        -------
            string:
                sensor identification.
        """
        pass

    @abstractmethod
    def get_measurement( self ):
        """The sensor reading measurement.

        Returns
        -------
            Measurement:
                measurement.
        """
        pass

if __name__ == '__main__':
    pass
