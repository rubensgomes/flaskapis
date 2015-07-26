"""rgapps.dao.sensordao module

This is where all the sensor database code is placed.
"""
import logging
import sqlite3

import arrow

from rgapps.config import ini_config
from rgapps.enums import DURATION_ENUM
from rgapps.utils.exception import IllegalArgumentException
from rgapps.utils.utility import dict_factory, is_blank, is_number


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["SensorDAO"]

class SensorDAO:
    """ Class API to provide sensor database API code
    """

    @staticmethod
    def add_measurement( unit, value, utc, serial ):
        """
        Adds given measurement data to sensor database

        Parameters
        ----------
        unit:  str (required)
            degF, degC, degF.
        value:  float (required)
            a float number
        utc: str (required)
            UTC timestamp of the reading
        serial: str (required)
            sensor unique serial number

        Returns
        -------
            nothing.
        """

        if is_blank( unit ):
            raise IllegalArgumentException( "unit is required." )

        if not value:
            raise IllegalArgumentException( "utc is required." )

        if not is_number( value ):
            raise IllegalArgumentException( "value is not a numeric value." )

        if is_blank( utc ):
            raise IllegalArgumentException( "utc is required." )

        if is_blank( serial ):
            raise IllegalArgumentException( "serial is required." )

        logging.debug( "Inserting measurement in database: "
                      "unit [{0}], value [{1}], utc [{2}], "
                      "serial [{3}]"
                      .format( unit, value, utc, serial ) )

        sql_db = ini_config.get( "SqlLite", "SQLITE_DB" )
        conn = sqlite3.connect( sql_db )
        logging.debug( "Connected to DB [{0}]".format( sql_db ) )

        c = conn.cursor()
        c.execute( "INSERT INTO readings (id, unit, value, utc, serial) "
                  "VALUES (?,?,?,?, ?)",
                  ( None, unit, value, utc, serial ) )

        conn.commit()
        logging.debug( "Measurement has been committed in database" )
        conn.close()

        logging.debug( "Disconnected from DB [{0}]".format( sql_db ) )

        return


    @staticmethod
    def get_sensor_information( serial ):
        """
        Returns a tuble corresponding to the sensor table in the database
        for the given sensor serial.

        Parameters
        ----------
        serial: str (required)
            sensor unique serial number

        Returns
        -------
        dict:
            A sensor dictionary containing column names as keys, and
            corresponding values.
        """

        if is_blank( serial ):
            raise IllegalArgumentException( "serial is required." )

        logging.debug( "Retrieving sensor with serial [{0}] from database."
                      .format( serial ) )

        sql_db = ini_config.get( "SqlLite", "SQLITE_DB" )
        conn = sqlite3.connect( sql_db )
        logging.debug( "Connected to DB [{0}]".format( sql_db ) )

        c = conn.cursor()
        c.row_factory = dict_factory
        cursor = c.execute( "SELECT * FROM sensor WHERE serial = '{0}'"
                           .format( serial ) )
        data = cursor.fetchone()

        conn.commit()
        conn.close()

        logging.debug( "Disconnected from DB [{0}]".format( sql_db ) )

        return data


    @staticmethod
    def get_sensor_readings( serial, duration ):
        """
        Returns .....

        Parameters
        ----------
        serial: str (required)
            sensor unique serial number
        duration: str (required)
            a valid DURATION_ENUM

        Returns
        -------
        dict:
            A sensor dictionary containing column names as keys, and
            corresponding values.
        """

        if is_blank( serial ):
            raise IllegalArgumentException( "serial is required." )

        if is_blank( duration ):
            raise IllegalArgumentException( "duration is required." )

        logging.debug( "Retrieving readings from sensor with serial [{0}] using "
                      "duration [{1}] from database."
                      .format( serial, duration ) )

        arrow_utcnow = arrow.utcnow()
        logging.debug( "current UTC now [{0}]".format( str( arrow_utcnow ) ) )

        arrow_utcpast = None


        if duration.lower().strip() == DURATION_ENUM.last5Years.name.lower():
            arrow_utcpast = arrow_utcnow.replace( years=-5 )
        elif duration.lower().strip() == DURATION_ENUM.last1Year.name.lower():
            arrow_utcpast = arrow_utcnow.replace( years=-1 )
        elif duration.lower().strip() == DURATION_ENUM.last6Months.name.lower():
            arrow_utcpast = arrow_utcnow.replace( months=-6 )
        elif duration.lower().strip() == DURATION_ENUM.last90Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace( days=-90 )
        elif duration.lower().strip() == DURATION_ENUM.last60Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace( days=-60 )
        elif duration.lower().strip() == DURATION_ENUM.last30Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace( days=-30 )
        elif duration.lower().strip() == DURATION_ENUM.last21Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace( days=-21 )
        elif duration.lower().strip() == DURATION_ENUM.last7Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace( days=-7 )
        elif duration.lower().strip() == DURATION_ENUM.last3Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace( days=-3 )
        elif duration.lower().strip() == DURATION_ENUM.lastDay.name.lower():
            arrow_utcpast = arrow_utcnow.replace( days=-1 )
        elif duration.lower().strip() == DURATION_ENUM.last24Hours.name.lower():
            arrow_utcpast = arrow_utcnow.replace( hours=-24 )
        elif duration.lower().strip() == DURATION_ENUM.last12Hours.name.lower():
            arrow_utcpast = arrow_utcnow.replace( hours=-12 )
        elif duration.lower().strip() == DURATION_ENUM.last6Hours.name.lower():
            arrow_utcpast = arrow_utcnow.replace( hours=-6 )
        elif duration.lower().strip() == DURATION_ENUM.lastHour.name.lower():
            arrow_utcpast = arrow_utcnow.replace( hours=-1 )
        else:
            raise IllegalArgumentException( "duration [{0}] is not valid"
                                           .format( duration ) )

        logging.debug( "current UTC [{0}], past UTC [{1}], duration[{2}]"
                      .format( str( arrow_utcnow ), str( arrow_utcpast ), duration ) )

        current_datetime = str( arrow_utcnow )
        past_datetime = str( arrow_utcpast )

        sql = ( "SELECT utc, unit, value FROM readings WHERE serial = '{0}' "
               "AND utc BETWEEN '{1}' AND '{2}' "
               "ORDER BY utc ASC"
               .format( serial, past_datetime, current_datetime ) )

        sql_db = ini_config.get( "SqlLite", "SQLITE_DB" )
        conn = sqlite3.connect( sql_db )
        logging.debug( "Connected to DB [{0}]".format( sql_db ) )

        c = conn.cursor()
        c.row_factory = dict_factory
        cursor = c.execute( sql )
        data = cursor.fetchall()

        conn.commit()
        conn.close()

        logging.debug( "Disconnected from DB [{0}]".format( sql_db ) )

        return data

