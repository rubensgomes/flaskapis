"""rgapps.domain.units.length module

This module contains the REST API source code for length conversions.
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["Length"]

from rgapps.enums import UNIT_TYPES_ENUM
from rgapps.domain.units import convert_unit
from rgapps.utils.utility import is_number


class Length:
    """to convert lengths
    """

    def convert(self, from_value, from_unit, to_unit):
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

        Raises
        ------
        ValueError if argument is invalid
        """
        if not is_number(from_value):
            raise ValueError(("Parameter from_value=[{0}] not valid. "
                              "A numeric value must be provided.")
                             .format(from_value))

        if not from_unit:
            raise ValueError(("Parameter from_unit=[{0}] not valid. "
                              "A unit be provided.")
                             .format(from_unit))

        if not to_unit:
            raise ValueError(("Parameter to_unit=[{0}] not valid. "
                              "A unit be provided.")
                             .format(to_unit))

        if from_unit == to_unit:
            raise ValueError(("from_unit=[{0}] and to_unit=[{1}] units "
                             "cannot be equal")
                             .format(from_unit, to_unit))

        # pint unit registry only accepts lower case letters for length units
        from_unit = from_unit.lower().strip()
        to_unit = to_unit.lower().strip()

        result = convert_unit(UNIT_TYPES_ENUM.length, from_unit,
                              from_value, to_unit)
        return result


if __name__ == "__main__":
    pass
