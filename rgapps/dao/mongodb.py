"""rgapps.dao.mongodb module

This is where some MongoDB utility code is placed.
"""
import logging

from pymongo import MongoClient

from rgapps.utils.exception import IllegalArgumentException
from rgapps.utils.utility import is_blank


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["MongoDB"]

class MongoDB:
    """ A class to provide MongoDB database API code
    """

    @staticmethod
    def _client(): #PRIVATE usage only!
        """
        Returns a valid and connected MongoClient object.

        Returns
        -------
        A MongoClient instance.

        Raises
        ------
        Raises MongoDB exception if MongoDB is not up and running, and the
        client could NOT connect to the database
        """

        # do not wait long to connect to the server
        # DO NOT set the timeout to 0(zero) as that will cause SocketException
        # when running Unit Testing having multiple threads.
        client = MongoClient(serverSelectionTimeoutMS=2)

        # run following call to check the server is up and running
        info = client.server_info()

        logging.debug("Connected to MongoDB [{0}] with info [{1}]."
                      .format(client, info))

        return client


    @staticmethod
    def database(name):
        """
        Returns a valid and connected Mongo Database object with
        the given name.

        Parameters:
        ----------
        name: str (required)
            the name of the MongoDB database

        Returns
        -------
        A Mongo Database instance.

        Raises
        ------
        Raises MongoDB exception if MongoDB is not up and running, and the
        client could NOT connect to the database
        """

        if is_blank(name):
            raise IllegalArgumentException("name is required.")

        client = MongoDB._client()

        db_found = False
        dbs = client.database_names()

        for db_name in dbs:
            if (db_name == name):
                db_found = True
                break

        if not db_found:
            client.close()
            raise IllegalArgumentException("MongoDB DB name [{0}] not found!"
                                           .format(name))

        db = client['{0}'.format(name)]

        logging.debug("MongoDB with database name [{0}] found."
                      .format(name))

        return db
