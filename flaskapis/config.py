"""flaskapis.config module

Contains initialization function that should be called to ensure the
environment is initialized properly
"""


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["set_up_environment"]


import errno
import logging
from logging.handlers import RotatingFileHandler
import os

from flask import current_app


def set_up_environment():
    """ Initializes configuration file, loggers.

    This method should only be called once at the start up of the
    application and after the Flask app instance has been created
    in order to initialize configuration file, logging.

    Raises
    ------

    EnvironmentError if there is a configuration missing or some other issues
    with the configuration file.
    """

    if "DEBUG" not in current_app.config:
        raise EnvironmentError("DEBUG property missing in application.cfg")

    if "TESTING" not in current_app.config:
        raise EnvironmentError("TESTING property missing in application.cfg")

    if "JSON_SORT_KEYS" not in current_app.config:
        raise EnvironmentError("JSON_SORT_KEYS property missing "
                               "in application.cfg")

    if "MAX_CONTENT_LENGTH" not in current_app.config:
        raise EnvironmentError("MAX_CONTENT_LENGTH property missing "
                               "in application.cfg")

    if "WORKING_DIR" not in current_app.config:
        raise EnvironmentError("WORKING_DIR property missing "
                               "in application.cfg")

    if "LOG_FILE" not in current_app.config:
        raise EnvironmentError("LOG_FILE property missing in application.cfg")

    if "LOG_FILE_MAX_BYTES" not in current_app.config:
        raise EnvironmentError("LOG_FILE_MAX_BYTES property missing "
                               "in application.cfg")

    if "LOG_BACKUP_COUNT" not in current_app.config:
        raise EnvironmentError("LOG_BACKUP_COUNT property missing "
                               "in application.cfg")

    if "LOG_LEVEL" not in current_app.config:
        raise EnvironmentError("LOG_LEVEL property missing in application.cfg")

    if "RESTFUL_APIS" not in current_app.config:
        raise EnvironmentError("RESTFUL_APIS property missing "
                               "in application.cfg")

    if "SQLITE_DB_ENABLE" not in current_app.config:
        raise EnvironmentError("SQLITE_DB_ENABLE property missing "
                               "in application.cfg")

    if "GMAIL_ACCOUNT" not in current_app.config:
        raise EnvironmentError("GMAIL_ACCOUNT property missing "
                               "in application.cfg")

    if "GMAIL_PASSWORD" not in current_app.config:
        raise EnvironmentError("GMAIL_PASSWORD property missing "
                               "in application.cfg")

    if current_app.config['SQLITE_DB_ENABLE']:
        if "SQLITE_DB" not in current_app.config:
            raise EnvironmentError("SQLITE_DB property missing "
                                   "in application.cfg")

    # ensure valid GMail Account
    from validate_email import validate_email
    is_valid = validate_email(current_app.config['GMAIL_ACCOUNT'].strip())

    if(not is_valid):
        raise EnvironmentError("GMail Account [{0}] is not valid email address"
                               .format(current_app.config['GMAIL_ACCOUNT']))

    # ensure working dir folder is available
    if not os.path.exists(current_app.config['WORKING_DIR'].strip()):
        os.makedirs(current_app.config['WORKING_DIR'].strip(), 0o775)

    # log file fullname including its path
    log_file_path = current_app.config['LOG_FILE'].strip()

    # Ensure log file is writeable
    log_file = open(log_file_path.encode("unicode-escape"), "w")
    log_file.close()

    # define the log level
    level = logging.INFO

    if current_app.config['LOG_LEVEL'].upper().strip() == "CRITICAL":
        level = logging.CRITICAL
    elif current_app.config['LOG_LEVEL'].upper().strip() == "ERROR":
        level = logging.ERROR
    elif current_app.config['LOG_LEVEL'].upper().strip() == "WARNING":
        level = logging.WARNING
    elif current_app.config['LOG_LEVEL'].upper().strip() == "INFO":
        level = logging.INFO
    elif current_app.config['LOG_LEVEL'].upper().strip() == "DEBUG":
        level = logging.DEBUG
    else:
        raise EnvironmentError(errno.EINVAL,
                               "LOG_LEVEL [{0}] not valid in application.cfg."
                               .format(current_app.config['LOG_LEVEL']))

    # create logging file handler
    log_file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=current_app.config['LOG_FILE_MAX_BYTES'],
        backupCount=current_app.config['LOG_BACKUP_COUNT']
        )
    log_file_handler.setLevel(level)

    # create logging formatter handler and add it to log handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "%m/%d/%Y %I:%M:%S %p"
        )
    log_file_handler.setFormatter(formatter)

    # add log handler to the Flask app.logger
    current_app.logger.addHandler(log_file_handler)

    # set the logging level to the application logger
    current_app.logger.setLevel(level)


if __name__ == '__main__':
    pass
