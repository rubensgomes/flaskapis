"""rgapps.utils.utility module

This module contains common utility functions.
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["get_log_file_handles", "is_number", "dict_factory",
           "decimal_places", "write_to_file"]


from decimal import Decimal


def dict_factory(cursor, row):
    """ a factory method used to construct the rows returned from SQLite

    Parameters
    ----------
    cursor: SQLite cursor
    row: SQLite row

    Returns
    -------
    dict:
        A dictionary containing column names as keys, and column values.
    """

    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d



def is_number(arg):
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
        float(arg)  # for int, long and float

    except ValueError:
        try:
            complex(arg)  # for complex
        except ValueError:
            return False

    return True


def decimal_places(arg):
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
    TypeError if argument is not numeric.
    """
    if not is_number(str(arg)):
        raise TypeError(("[{0}] is not a number").format(arg))

    dec = Decimal(str(arg))
    exp = dec.as_tuple().exponent
    result = -exp

    return result


def write_to_file(msg, fileToWrite):
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
        fileToWrite.write(msg)

    return


def get_log_file_handles(logger):
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
            handles.append(handler.stream.fileno())

        if logger.parent:
            handles += get_log_file_handles(logger.parent)

    return handles



if __name__ == '__main__':
    pass
