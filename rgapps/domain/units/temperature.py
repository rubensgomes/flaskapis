"""rgapps.domain.units.temperature module

This module contains the temperature conversions.
"""

from rgapps.enums import UNIT_TYPES_ENUM
from rgapps.utils.exception import IllegalArgumentException
from rgapps.utils.utility import is_number, is_blank, convert_unit


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["Temperature"]



class Temperature:
    """to convert temperatures
    """

    @staticmethod
    def convert( from_value, from_unit, to_unit ):
        """convert length units.

        Parameters
        ----------
        from_value:  str (required)
            numeric value
        from_unit:  str (required)
            length unit
        to_unit:  str (required)
            length unit

        Returns
        -------
        float:
            the converted value
        """
        if not is_number( from_value ):
            raise IllegalArgumentException( 
                ( "Parameter from_value=[{0}] not valid. "
                 "A numeric value must be provided." ).format( from_value ) )

        if is_blank( from_unit ):
            raise IllegalArgumentException( 
                ( "Parameter from_unit=[{0}] not valid. A unit be provided." )
                .format( from_unit ) )

        if is_blank( to_unit ):
            raise IllegalArgumentException( 
                ( "Parameter to_unit=[{0}] not valid. A unit be provided." )
                .format( to_unit ) )

        if from_unit == to_unit:
            raise IllegalArgumentException( 
                ( "from_unit=[{0}] and to_unit=[{1}] units cannot be equal" )
                .format( from_unit, to_unit ) )

        # pint temperature units need to be lower-cased or degC, degF, degK
        from_unit = from_unit.lower().strip()
        if from_unit == "degc":
            from_unit = "degC"
        elif from_unit == "degf":
            from_unit = "degF"
        elif from_unit == "degk":
            from_unit = "degK"

        # pint temperature units need to be lower-cased or degC, degF, degK
        to_unit = to_unit.lower().strip()
        if to_unit == "degc":
            to_unit = "degC"
        elif to_unit == "degf":
            to_unit = "degF"
        elif to_unit == "degk":
            to_unit = "degK"

        result = convert_unit( UNIT_TYPES_ENUM.temperature, from_unit,
                              from_value, to_unit )
        return result


if __name__ == "__main__":
    pass
