"""rgapps.utils.utility module

This module contains common utility functions.
"""
from decimal import Decimal
import logging

from pint.unit import UnitRegistry, UnitsContainer

from rgapps.enums import UNIT_TYPES_ENUM
from rgapps.utils.exception import IllegalArgumentException


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["get_log_file_handles", "is_number", "dict_factory",
           "decimal_places", "write_to_file", "isNotBlank",
           "convert_unit"]


def convert_unit( unit_type, from_unit, from_value, to_unit ):
    """Converts value/unit found in params to the given to_unit.

    It validates the input parameters to ensure that they
    contain the expected types of data.  Then, it converts
    the given unit value to the requested to_unit.  And it
    returns the converted result.

    Parameters
    ----------
    unit_type: UNIT_TYPES_ENUM (required)
        It  is a valid pint unit type
    from_unit: str (required)
        It is a valid pint unit to be converted from.
    from_value: float (required)
        It is a number corresponding to the from_unit to be converted from.
    to_unit : str (required)
        It is a valid pint unit to be converted to.

    Returns
    -------
    float:
        the converted unit value.
    """

    if not unit_type:
        raise IllegalArgumentException( "unit_type is required." )

    if not isinstance( unit_type, UNIT_TYPES_ENUM ):
        raise IllegalArgumentException( "unit_type is not UNIT_TYPES_ENUM." )

    if is_blank( from_unit ):
        raise IllegalArgumentException( "from_unit is required." )

    if not from_value :
        raise IllegalArgumentException( "from_value is required." )

    if not is_number( from_value ):
        raise IllegalArgumentException( "from_value [{0}] is not a number."
                                        .format( from_value ) )

    if is_blank( to_unit ):
        raise IllegalArgumentException( "to_unit is required." )


    # pint unit_reg unit converter object
    unit_reg = UnitRegistry( autoconvert_offset_to_baseunit=True )

    # an exception is raised if the to_unit is not valid
    to_unit_name = unit_reg.get_name( to_unit )
    to_unit_dimension = unit_reg.get_dimensionality( to_unit_name )

    if to_unit_dimension != UnitsContainer( {"[" + unit_type.name + "]": 1} ):
        raise IllegalArgumentException( 
            ( "Parameter to_unit=[{0}] not valid. [{1}] unit required." )
            .format( to_unit, unit_type.name ) )

    # an exception is raised if the from_unit is not valid
    from_unit_name = unit_reg.get_name( from_unit )
    from_unit_dimension = unit_reg.get_dimensionality( from_unit_name )

    if from_unit_dimension != UnitsContainer( {"[" + unit_type.name + "]": 1} ):
        raise IllegalArgumentException( 
            ( "Parameter from_unit=[{0}] not valid. [{1}] unit required." )
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

    logging.debug( "input [{0} {1}] result [{2} {3}]"
                  .format( from_value, from_unit_name, result, to_unit_name ) )

    return final_result



def is_blank ( arg ):
    """ A simple method to check if a string is null or blank.

    Parameters
    ----------
    arg: string
        must be a string object.

    Returns
    -------
    True: if it is a blank string
    False: if it string is not blank

    """
    if not arg:
        return True

    if not isinstance( arg, basestring ):
        raise IllegalArgumentException( "arg must be a string." )

    if arg.strip():
        return False

    return True



def dict_factory( cursor, row ):
    """ a factory method used to construct the rows returned from SQLite

    Parameters
    ----------
    cursor: SQLite cursor (required)
    row: SQLite row

    Returns
    -------
    dict:
        A dictionary containing column names as keys, and column values.
    """
    if not cursor:
        raise IllegalArgumentException( "cursos is required." )

    d = {}

    for idx, col in enumerate( cursor.description ):
        d[col[0]] = row[idx]

    return d



def is_number( arg ):
    """
    Checks if arg is a number.

    Parameters
    ----------
    arg: string
        An argument that wants to check to see if it is a number.
        A number can be float, int or complex.

    Returns
    -------
    True: if it is a number
    False: if it is not a number
    """
    if not arg:
        return False

    try:
        float( arg )  # for int, long and float

    except ValueError:
        try:
            complex( arg )  # for complex
        except ValueError:
            return False

    return True


def decimal_places( arg ):
    """
    Returns the number of decimal places in the given number

    Parameters
    ----------
    arg: Numeric or string
        A number to determine the number of decimal places

    Returns
    -------
    Number of decimal places found.

    Raises
    ------
    IllegalArgumentException if argument is not numeric.
    """

    if not is_number( str( arg ) ):
        raise IllegalArgumentException( ( "[{0}] is not a number" )
                                        .format( arg ) )

    dec = Decimal( str( arg ) )
    exp = dec.as_tuple().exponent
    result = -exp

    return result


def write_to_file( msg, fileToWrite ):
    """ Simple utility to write to file.

    It is to replace the following that has been deprecated in Python 3.4:
        print >> file, "some text

    Parameters
    ----------
    msg: string (optional)
        A text message
    fileToWrite: file (required)
        An existing writeable file

    Returns
    -------
    Nothing
    """

    if fileToWrite and not fileToWrite.closed:
        fileToWrite.write( msg )

    return


def get_log_file_handles( logger ):
    """ Returns a list of the file descriptors used by the given
    logging.logger.  This method may be used by the DaemonContext
    files_preserve when creating daemon on Linux environment.

    Parameters
    ----------
    logger: logging.logger (ooptional)

    Returns
    -------
    List containing all the file handle descriptors used by the given logger.
    """
    handles = []

    if logger:

        for handler in logger.handlers:
            handles.append( handler.stream.fileno() )

        if logger.parent:
            handles += get_log_file_handles( logger.parent )

    return handles



if __name__ == '__main__':
    pass
