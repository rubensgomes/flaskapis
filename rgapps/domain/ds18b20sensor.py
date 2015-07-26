"""rgapps.domain.ds18b20sensor module

This is where all the Dallas Semiconductor DS18B20 sensor domain code is
placed.
"""
import logging

import arrow
from pint.unit import UnitRegistry
from w1thermsensor import ( W1ThermSensor, NoSensorFoundError,
                           SensorNotReadyError, UnsupportedUnitError )

from rgapps.config import ini_config
from rgapps.domain.sensor import Sensor, Measurement
from rgapps.enums import TEMPERATURE_ENUM, UNIT_TYPES_ENUM
from rgapps.utils.exception import IllegalArgumentException, \
    SensorReadingException
from rgapps.utils.utility import decimal_places, is_blank, convert_unit


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["DS18B20Sensor"]



DEFAULT_TEMPERATURE_UNIT = TEMPERATURE_ENUM.degC

class DS18B20Sensor ( Sensor ):
    """Dallas Semiconductor DS18B20 1-Wire Digital Temperature Sensor.
    """

    def __init__( self, serial ):
        """constructor.
        Parameters
        ----------
        serial:  str (required)
            sensor serial or identification string
        """
        if is_blank( serial ):
            raise IllegalArgumentException( "serial is required." )

        self.serial = serial


    def get_serial( self ):
        """ concrete implementation of abstract method in Sensor
        """
        return self.serial


    def get_measurement( self ):
        """ concrete implementation of abstract method in Sensor
        """
        is_testing = ini_config.getboolean( "Flask", "TESTING" )
        if is_testing is True:
            logging.debug( "Using a testing temperature from sensor [{0}]."
                          .format( self.serial ) )
            temperature = 100
        else:
            logging.debug( "Reading temperature from sensor [{0}]."
                          .format( self.serial ) )
            temperature = self.__get_sensor_temperature( self.serial )

        logging.debug( "Sensor temperature in [{0}] is [{1}]"
                       .format( DEFAULT_TEMPERATURE_UNIT.name, temperature ) )

        # use pint to represent temperature
        unit_reg = UnitRegistry( autoconvert_offset_to_baseunit=True )

        temperature_qty = temperature * unit_reg( DEFAULT_TEMPERATURE_UNIT.name )

        # restrict results to 2 decimal places.
        decimals = decimal_places( temperature_qty.magnitude )
        if( decimals > 2 ):
            temperature_result = round( temperature_qty.magnitude, 2 )
        else:
            temperature_result = temperature_qty.magnitude

        utc = arrow.utcnow()

        reading = Measurement( temperature_result,
                              DEFAULT_TEMPERATURE_UNIT.name,
                              str( utc ) )
        return reading


    def __get_sensor_temperature( self, serial ):
        """ Private method used to retrieve temperature from real sensor
        """
        ds18b20Sensor = None
        logging.debug( "Reading temperature from DS18B20 sensor "
                      "with Serial [{0}]".format( serial ) )

        try:
            ds18b20Sensor = W1ThermSensor( W1ThermSensor.THERM_SENSOR_DS18B20,
                                          serial )
            logging.debug( "Instantiated DS18B20 temperature sensor "
                          "with Serial [{0}]"
                          .format( serial ) )

            if ( DEFAULT_TEMPERATURE_UNIT == TEMPERATURE_ENUM.degC ):
                temperature = ds18b20Sensor.get_temperature( 
                                                    W1ThermSensor.DEGREES_C )
            elif ( DEFAULT_TEMPERATURE_UNIT == TEMPERATURE_ENUM.degK ):
                degF_temperature = ds18b20Sensor.get_temperature( 
                                                    W1ThermSensor.DEGREES_F )
                # sensor only supports Celsius and Fahrenheit.
                # We should therefore use pint to convert to Kelvin
                logging.debug( "Kevin unit is not supporte by sensor "
                              "with serial [{0}]. Using pint to "
                              "convert [{1}] to degK"
                              .format( serial, degF_temperature ) )
                temperature = convert_unit( UNIT_TYPES_ENUM.temperature,
                                           TEMPERATURE_ENUM.degF,
                                           temperature,
                                           TEMPERATURE_ENUM.degK )
            elif ( DEFAULT_TEMPERATURE_UNIT == TEMPERATURE_ENUM.degF ):
                temperature = ds18b20Sensor.get_temperature( 
                    W1ThermSensor.DEGREES_F )
            else:
                # should never get here (sanity only).
                raise Exception( "Invalid [{0}]"
                                .format( DEFAULT_TEMPERATURE_UNIT ) )

        except NoSensorFoundError as err:
            msg = ( "Sensor with serial [{0}] not found. Error [{1}]."
                    .format( serial, err ) )
            logging.warn( msg )
            raise SensorReadingException( msg )

        except SensorNotReadyError as err:
            msg = ( "Sensor with serial [{0}] not ready yet. Error [{1}]."
                   .format( serial, err ) )
            logging.warn( msg )
            raise SensorReadingException( msg )

        except UnsupportedUnitError as err:
            msg = ( "Sensor with serial [{0}] does not support requested unit."
                   " Error [{1}]"
                   .format( serial, err ) )
            logging.warn( msg )
            raise SensorReadingException( msg )

        return temperature

if __name__ == '__main__':
    pass
