"""rgapps.enums module

This is a placeholder to place global Enums
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["DURATION_ENUM", "MIME_TYPE_ENUM", "SENSOR_TYPE_ENUM",
           "SENSOR_STATE_ENUM", "TEMPERATURE_ENUM", "UNIT_TYPES_ENUM"]


from enum import Enum


class MIME_TYPE_ENUM(Enum):
    """An enumeration of MIME_TYPE_ENUM

    This class implements an enumeration of possible MimeTypes.
    """
    HTML = 1
    XML = 2
    CSV = 3
    JSON = 4


class TEMPERATURE_ENUM(Enum):
    """ An enumeration of temperature units

    This class implements an enumeartiof of possible sensor temperature units.
    Do NOT change the enum names because they must map to what is being used
    by the pint library.
    """
    degC = 1
    degF = 2
    degK = 3

    @staticmethod
    def unit_name(temperature):
        """ Returns the official unit name.

        Parameters:
        ----------
        temperature: TEMPERATURE_ENUM or str (required)
            a TEMPERATURE_ENUM or text string with "pint" temperature name

        Returns:
        -------
        Official temperature name.
        """
        if temperature and isinstance(temperature, TEMPERATURE_ENUM):
            if temperature == TEMPERATURE_ENUM.degC:
                return "celsius"
            elif temperature == TEMPERATURE_ENUM.degF:
                return "fahrenheit"
            elif temperature == TEMPERATURE_ENUM.degK:
                return "kevin"
            else:
                raise Exception(
                   "temperature [{0}] is not valid"
                   .format(temperature))
        elif temperature:
            for t in TEMPERATURE_ENUM:
                if t.name.lower() == temperature.lower().strip():
                    return TEMPERATURE_ENUM.unit_name(t)
            raise Exception("temperature [{0}] is not valid"
                            .format(temperature))
        else:
            raise Exception("temperature [{0}] is not valid"
                            .format(temperature))



class UNIT_TYPES_ENUM(Enum):
    """A enumeration of valid pint unit types.

    This class represents a list of pint unit types.  Do not change this,
    unless the pint library code also changes.
    """
    length = 1
    mass = 2
    temperature = 3


class DURATION_ENUM(Enum):
    """ Duration of intervals to query historical information.
    """
    last5Years = 1
    last1Year = 2
    last6Months = 3
    last90Days = 4
    last60Days = 5
    last30Days = 6
    last21Days = 7
    last7Days = 8
    last3Days = 9
    lastDay = 10
    last24Hours = 11
    last12Hours = 12
    last6Hours = 13
    lastHour = 14

    @staticmethod
    def is_valid(duration):
        """ Checks if the given duration is valid.

        Parameters:
        ----------
        duration: str (optional)
            a possible duration string

        Returns:
        -------
        True if duration is valid; False, otherwise.
        """
        for d in DURATION_ENUM:
            if d.name.lower() == duration.lower().strip():
                return True

        return False


class SENSOR_TYPE_ENUM(Enum):
    """An enumeration of Sensor types

    This class implements an enumeration of possible sensor types.
    """
    TEMPERATURE = 1
    HUMIDITY = 2


class SENSOR_STATE_ENUM(Enum):
    """An enumeration of Sensor Status

    This class implements an enumeration of possible sensor status.
    """
    DOWN = 1
    UP = 2
    DISCONNECTED = 3
    UNKNOWN = 4


if __name__ == '__main__':
    pass
