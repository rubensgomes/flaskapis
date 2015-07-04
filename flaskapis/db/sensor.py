"""flaskapis.db.sensor module

This is where all the sensor database code is place.
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["SensorDb"]

import sqlite3

import arrow
from flask import current_app, g

from flaskapis.enums import DURATION_ENUM
from werkzeug.exceptions import BadRequest


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


class SensorDb:
    """ Class API to update sensor database tables
    """

    def add_measurement(self, unit, value, utc, serial):
        """
        Adds given measurement data to sensor database

        Parameters
        ----------
        unit:  str (required)
            degF, degC, degF.
        value:  real (required)
            a real number
        utc: str (required)
            UTC timestamp of the reading
        serial: str (required)
            sensor unique serial number

        Returns
        -------
            nothing.
        """

        current_app.logger.debug("Inserting measurement in database: "
                                 "unit [{0}], value [{1}], utc [{2}], "
                                 "serial [{3}]"
                                 .format(unit, value, utc, serial))

        db = getattr(g, 'db', None)
        if db is None:
            g.db = sqlite3.connect(current_app.config['SQLITE_DB'])
            current_app.logger.debug("Connected to DB [{0}]"
                                     .format(current_app.config['SQLITE_DB']))

        c = g.db.cursor()
        c.execute("INSERT INTO readings (id, unit, value, utc, serial) "
                  "VALUES (?,?,?,?, ?)",
                  (None, unit, value, utc, serial))
        g.db.commit()

        current_app.logger.debug("Measurement has been committed in database")

        return


    def get_sensor_information(self, serial):
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

        current_app.logger.debug("Retrieving sensor with serial [{0}] "
                                 "from database."
                                 .format(serial))

        connection = g.db.cursor()
        connection.row_factory = dict_factory
        cursor = connection.execute("SELECT * FROM sensor WHERE serial = '{0}'"
                                    .format(serial))
        data = cursor.fetchone()
        g.db.commit()

        return data


    def get_sensor_readings(self, serial, duration):
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

        current_app.logger.debug(
            "Retrieving readings from sensor with serial [{0}] using "
            "duration [{1}] from database.".format(serial, duration))

        arrow_utcnow = arrow.utcnow()
        current_app.logger.debug("current UTC now [{0}]"
                                 .format(str(arrow_utcnow)))

        arrow_utcpast = None


        if duration.lower().strip() == DURATION_ENUM.last5Years.name.lower():
            arrow_utcpast = arrow_utcnow.replace(years=-5)
        elif duration.lower().strip() == DURATION_ENUM.last1Year.name.lower():
            arrow_utcpast = arrow_utcnow.replace(years=-1)
        elif duration.lower().strip() == DURATION_ENUM.last6Months.name.lower():
            arrow_utcpast = arrow_utcnow.replace(months=-6)
        elif duration.lower().strip() == DURATION_ENUM.last90Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-90)
        elif duration.lower().strip() == DURATION_ENUM.last60Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-60)
        elif duration.lower().strip() == DURATION_ENUM.last30Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-30)
        elif duration.lower().strip() == DURATION_ENUM.last21Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-21)
        elif duration.lower().strip() == DURATION_ENUM.last7Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-7)
        elif duration.lower().strip() == DURATION_ENUM.last3Days.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-3)
        elif duration.lower().strip() == DURATION_ENUM.lastDay.name.lower():
            arrow_utcpast = arrow_utcnow.replace(days=-1)
        elif duration.lower().strip() == DURATION_ENUM.last24Hours.name.lower():
            arrow_utcpast = arrow_utcnow.replace(hours=-24)
        elif duration.lower().strip() == DURATION_ENUM.last12Hours.name.lower():
            arrow_utcpast = arrow_utcnow.replace(hours=-12)
        elif duration.lower().strip() == DURATION_ENUM.last6Hours.name.lower():
            arrow_utcpast = arrow_utcnow.replace(hours=-6)
        elif duration.lower().strip() == DURATION_ENUM.lastHour.name.lower():
            arrow_utcpast = arrow_utcnow.replace(hours=-1)
        else:
            raise BadRequest("duration [{0}] is not valid".format(duration))

        current_app.logger.debug(
            "current UTC [{0}], past UTC [{1}], duration[{2}]"
            .format(str(arrow_utcnow), str(arrow_utcpast), duration))

        current_datetime = str(arrow_utcnow)
        past_datetime = str(arrow_utcpast)

        sql = ("SELECT utc, unit, value FROM readings WHERE serial = '{0}' "
               "AND utc BETWEEN '{1}' AND '{2}' "
               "ORDER BY utc ASC"
               .format(serial, past_datetime, current_datetime))

        connection = g.db.cursor()
        connection.row_factory = dict_factory
        cursor = connection.execute(sql)

        data = cursor.fetchall()
        g.db.commit()

        return data


if __name__ == '__main__':
    pass
