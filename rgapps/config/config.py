"""rgapps.config module

Contains initialization configuration code to load the properties defined in
the configuration INI file.
"""

import errno
import logging
from logging.handlers import RotatingFileHandler
import os

from rgapps.constants import  INI_FILE
from rgapps.config import ini_config

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["initialize_environment"]


def initialize_environment(log_file_path=None):
    """ Loads the configuration file and initializes logging.

    This method should only be called once at the start up of the
    application to read in the configuration file, and set up logging.
    """

    print("Loading config file [{0}]".format(INI_FILE))
    ini_config.read(INI_FILE)

    # ensure working dir folder is available
    working_dir = ini_config.get("Logging", "WORKING_DIR")
    if not os.path.exists(working_dir):
        os.makedirs(working_dir, 0o775)

    # log file fullname including its path
    if log_file_path is None:
        log_file_path = ini_config.get("Logging", "LOG_FILE")

    # ensure log file is writeable
    log_file = open(log_file_path.encode("unicode-escape"), "w")
    log_file.close()

    max_bytes = ini_config.get("Logging", "LOG_FILE_MAX_BYTES")
    backup_count = ini_config.get("Logging", "LOG_BACKUP_COUNT")
    log_level = ini_config.get("Logging", "LOG_LEVEL")

    # define the log level
    level = logging.INFO

    if log_level.upper().strip() == "CRITICAL":
        level = logging.CRITICAL
    elif log_level.upper().strip() == "ERROR":
        level = logging.ERROR
    elif log_level.upper().strip() == "WARNING":
        level = logging.WARNING
    elif log_level.upper().strip() == "INFO":
        level = logging.INFO
    elif log_level.upper().strip() == "DEBUG":
        level = logging.DEBUG
    else:
        raise EnvironmentError(errno.EINVAL,
                               "LOG_LEVEL [{0}] not valid in [{1}]."
                               .format(log_level, log_file_path))

    # create logging file handler
    log_file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=max_bytes,
        backupCount=backup_count
        )
    log_file_handler.setLevel(level)

    log_format = "%(asctime)s - %(name)s - %(func):%(lineno) - %(levelname)s - %(message)s"
    date_fmt = "%m/%d/%Y %I:%M:%S %p"

    # create logging formatter handler and add it to log handler
    formatter = logging.Formatter(log_format, date_fmt)
    log_file_handler.setFormatter(formatter)

    logging.getLogger().addHandler(log_file_handler)
    logging.getLogger().setLevel(level)

    print("Logs are being set to [{0}]".format(log_file_path))

    return


if __name__ == '__main__':
    pass
