"""rgapss.domain.units subpackage

Sub-package containing units conversion code

Modules:
-------
length: a module containing length converting code.
temperature: a module containing temperature  converting code.
weight: a module containing weight converting code.

Sub-Packages:
------------
None
"""
from collections import OrderedDict
from distutils.tests.support import LoggingSilencer
import logging

from pint.unit import UnitRegistry, UnitsContainer
import pkg_resources

from rgapps.constants import ( 
    DATA_KEY, STATUS_KEY, STATUS_SUCCESS
    )
from rgapps.utils.utility import decimal_places


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["convert_unit", "length", "temperature", "weight"]


def convert_unit( unit_type, from_unit, from_value, to_unit ):
    """Converts value/unit found in params to the given to_unit.

    It validates the input parameters to ensure that they
    contain the expected types of data.  Then, it converts
    the given unit value to the requested to_unit.  And it
    returns the converted result.

    Parameters
    ----------
    unit_type: str (required)
        It  is a valid pint unit type
    from_unit: str (required)
        It is a valid pint unit to be converted from.
    from_value: str (required)
        It is a number corresponding to the from_unit to be converted from.
    to_unit : str (required)
        It is a valid pint unit to be converted to.

    Returns
    -------
    dict:
        An ordered dictionary containing the from unit/value and to
        unit/value along with status.

    Raises
    ------
    BadRequest if if there is an error validating the input parameters.
    """
    # pint unit_reg unit converter object
    unit_reg = UnitRegistry( autoconvert_offset_to_baseunit=True )

    # an exception is raised if the to_unit is not valid
    to_unit_name = unit_reg.get_name( to_unit )
    to_unit_dimension = unit_reg.get_dimensionality( to_unit_name )

    if to_unit_dimension != UnitsContainer( {"[" + unit_type.name + "]": 1} ):
        raise ValueError( ( "Parameter to_unit=[{0}] not valid. "
                         "A [{1}] unit must be provided." )
                        .format( to_unit, unit_type.name ) )

    # an exception is raised if the from_unit is not valid
    from_unit_name = unit_reg.get_name( from_unit )
    from_unit_dimension = unit_reg.get_dimensionality( from_unit_name )

    if from_unit_dimension != UnitsContainer( {"[" + unit_type.name + "]": 1} ):
        raise ValueError( "Parameter from_unit=[{0}] not valid. "
                         "A [{1}] unit must be provided."
                        .format( from_unit, unit_type.name ) )

    logging.debug( "converting [{0} {1}] to [{2}]"
                  .format( from_value, from_unit_name, to_unit_name ) )

    from_value_float = float( from_value )
    from_value_quantity = from_value_float * unit_reg( from_unit_name )

    to_value_quantity = from_value_quantity.to( unit_reg( to_unit_name ) )

    result = to_value_quantity.magnitude
    decimals = decimal_places( to_value_quantity.magnitude )

    final_result = result
    # restrict results to 2 decimal places.
    if( decimals > 2 ):
        final_result = round( result, 2 )

    if final_result == 0:
        # do not return 0 (zero) when rounding gives 0 value.
        final_result = result

    # convert the string type of from_value to a number type
    if len( set( ['.', 'e', 'E'] ).intersection( from_value ) ) > 0:
        from_value = float( from_value )
    else:
        from_value = int( from_value )

    logging.debug( "input [{0} {1}] result [{2} {3}]"
                  .format( from_value, from_unit_name, result, to_unit_name ) )

    data = OrderedDict()
    data["from_unit"] = from_unit
    data["from_value"] = from_value
    data["to_unit"] = to_unit
    data["to_value"] = final_result

    response = OrderedDict()
    response[STATUS_KEY] = STATUS_SUCCESS
    response[DATA_KEY] = data

    return response


if __name__ == '__main__':
    pass
