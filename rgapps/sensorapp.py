"""rgapps.sensorapp background daemon job

This program collects data from sensors periodically and store the
readings in the database.
"""
import logging
import platform
import signal
import sys
import time

from flask.app import Flask
import requests
from requests.exceptions import ( ConnectionError, Timeout,
                                 RequestException, HTTPError )

from rgapps.config import ini_config
from rgapps.config.config import initialize_environment
from rgapps.dao.sensordao import SensorDAO
from rgapps.domain.myemail import EMail
from rgapps.utils.constants import SENSOR_KEY, DATA_KEY
from rgapps.utils.utility import write_to_file


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"


INI_FILE = r"/home/wsgi/sensorserver/application.ini"

# global variable: to be defined in run()
globalFlaskApp = None


def read_store_readings ():
    """ Function used to read and store sensor readings
    """

    if not globalFlaskApp:
        raise EnvironmentError( "Flask has not been initialized" )

    # error flag used to send email only once if error occurs.
    error_flag = False

    headers = {'content-type': 'application/json'}

    sensor_url = ini_config.get( "Sensor", "SENSOR_TEMPERATURE_URL" )
    sensor_serial = ini_config.get( "Sensor", "SENSOR_TEMPERATURE_SERIAL" )

    rest_url = ( sensor_url + "/" + sensor_serial )
    rest_user = ini_config.get( "Sensor", "SENSOR_REST_API_USERNAME" )
    rest_pw = ini_config.get( "Sensor", "SENSOR_REST_API_PASSWORD" )
    req_timeout = ini_config.getint( "Sensor", "SENSOR_REQUEST_TIMEOUT" )
    sleep_timeout = ini_config.getint( "Sensor", "SENSOR_SLEEP_TIME" )
    recipient = ini_config.get( "Email", "RECIPIENT_EMAIL" )

    with globalFlaskApp.app_context():

        # start daemon forever loop
        while True:

            try:
                # collect data from sensor using RESTFul API
                logging.debug( "Sending request to [{0}] with user [{1}]"
                               .format( rest_url, rest_user ) )

                r = requests.get( rest_url,
                                 verify=False,
                                 auth=( rest_user, rest_pw ),
                                 headers=headers,
                                 timeout=req_timeout )

                # if code gets here no exception has occurred. reset flag.
                error_flag = False

                if ( r.status_code != 200 ):
                    logging.error( "Response status code [{0}] : [{1}]"
                                   .format( r.status_code, r.text ) )
                else:
                    output = r.json()
                    sensor = output[SENSOR_KEY]
                    readings = output[DATA_KEY]

                    logging.debug( "Adding sensor record with unit [{0}], "
                                   "value [{1}], utc [{2}], serial [{3}] to "
                                   "database."
                                   .format( readings["unit"],
                                            readings["value"],
                                            readings["utc"],
                                            sensor["serial"] ) )

                    SensorDAO.add_measurement( readings["unit"],
                                               readings["value"],
                                               readings["utc"],
                                               sensor["serial"] )

            # python 3.4: ConnectionRefusedError
            except ( ConnectionError, Timeout ) as err:  # e.g., server is down.
                sys.stderr.write( str( err ) )

                logging.exception( "Connection Error with URL [{0}], "
                                   "user [{1}] in runserver daemon: [{2}]"
                                   .format( rest_url, rest_user, err ) )

                if not error_flag :  # only send email once.
                    subject = "sensorserver: Connection/Timeout Error"
                    logging.info( "Sending email to [{0}] with subject [{1}]"
                                  .format( recipient, subject ) )
                    message = ( "Connection/Timeout Error to URL [{0}]: [{1}]"
                               .format( rest_url, err ) )
                    try:
                        EMail.send_email( recipient, subject, message )
                        logging.info( "email to [{0}] with subject [{1}] sent."
                                      .format( recipient, subject ) )
                    except Exception as mail_err:
                        logging.error( "Error [{0}] sending email."
                                       .format( mail_err ) )

                error_flag = True

            except ( HTTPError, RequestException ) as err:
                sys.stderr.write( str( err ) )

                logging.exception( "HTTP/Request Error to URL [{0}] in "
                                   "runserver daemon: [{1}]"
                                   .format( rest_url, err ) )

                if not error_flag :  # only send email once.
                    subject = "sensorserver: HTTP Error"
                    logging.info( "Sending email to [{0}] with subject [{1}]"
                                  .format( recipient, subject ) )
                    message = ( "HTTP/Request to URL [{0}] Error: [{1}]"
                               .format( rest_url, err ) )

                    try:
                        EMail.send_email( recipient, subject, message )
                        logging.info( 
                            "email to [{0}] with subject [{1}] was sent."
                            .format( recipient, subject ) )
                    except Exception as mail_err:
                        logging.error( "Error [{0}] sending email."
                                       .format( mail_err ) )

                error_flag = True

            except ( EnvironmentError, Exception ) as err:
                sys.stderr.write( str( err ) )

                logging.exception( "Error in runserver daemon: [{0}]"
                                   .format( err ) )

                if not error_flag :  # only send email once.
                    subject = "sensorserver: Environment Error"
                    logging.info( "Sending email to [{0}] with subject [{1}]"
                                  .format( recipient, subject ) )
                    message = "EXITING APPLICATION. Error: [{0}]".format( err )

                    try:
                        EMail.send_email( recipient, subject, message )
                        logging.info( 
                            "email to [{0}] with subject [{1}] was sent."
                            .format( recipient, subject ) )
                    except Exception as mail_err:
                        logging.error( "Error [{0}] sending email."
                                       .format( mail_err ) )

                error_flag = True

            except:  # catch *all* other exceptions
                err = sys.exc_info()[0]
                logging.exception( "Error occurred in runserver daemon: [{0}]"
                                   .format( err ) )

                write_to_file( "<p>Error in runsensor daemon: [{0}]</p>"
                              .format( err ), sys.stderr )
                exit( 1 )


            time.sleep( sleep_timeout )

    return

def program_cleanup( signum, frame ):
    """ daemon cleanup code run on Linux when handling SIGTERM (15) signal
    """

    if not globalFlaskApp:
        raise EnvironmentError( "Flask has not been initialized" )

    with globalFlaskApp.app_context():
        logging.info( "Program terminating with signum [{0}] under Linux."
                      .format( signum ) )
    exit( 0 )


def run():
    """ daemon run function.

    This function should be called to start the system.
    """

    print( "initializing the environment..." )
    initialize_environment( INI_FILE )

    instance_path = ini_config.get( "Flask", "INSTANCE_PATH" )

    # app: Flask application object
    global globalFlaskApp
    globalFlaskApp = Flask( __name__,
                            instance_path=instance_path,
                            instance_relative_config=True )

    is_debug = ini_config.getboolean( "Flask", "DEBUG" )
    is_testing = ini_config.getboolean( "Flask", "TESTING" )
    is_json_sort_keys = ini_config.getboolean( "Flask", "JSON_SORT_KEYS" )
    max_content_length = ini_config.getint( "Flask", "MAX_CONTENT_LENGTH" )

    globalFlaskApp.config.update( DEBUG=is_debug,
                                  TESTING=is_testing,
                                  JSON_SORT_KEYS=is_json_sort_keys,
                                  MAX_CONTENT_LENGTH=max_content_length )


    with globalFlaskApp.app_context():

        logging.info( "Starting application ..." )

        from rgapps.utils.utility import get_log_file_handles
        logger_fds = get_log_file_handles( logging.getLogger() )
        logging.debug( "Logger file handles fileno [{0}]"
                       .format( logger_fds ) )

        system = platform.system()

        if system == "Linux":
            logging.info( "Server running on Linux." )

            pid_file = ini_config.get( "Sensor", "SENSOR_PID_FILE" )
            working_dir = ini_config.get( "Logging", "WORKING_DIR" )

            logging.debug( "Instantiating daemon with pid_file [{0}] "
                           "and working_dir [{1}]"
                           .format( pid_file, working_dir ) )

            import daemon.pidfile

            daemon_context = daemon.DaemonContext( 
                working_directory=working_dir,
                umask=0o002,
                pidfile=daemon.pidfile.PIDLockFile( pid_file ) )

            logging.debug( "Setting up daemon signal map" )
            daemon_context.signal_map = { signal.SIGTERM: program_cleanup }
            logging.debug( "daemon signal map has been setup" )

            if ( logger_fds ):
                logging.debug( "setting files_preserve for the log file "
                               "descriptor [{0}]"
                               .format( logger_fds ) )
                daemon_context.files_preserve = logger_fds

            logging.debug( "Starting daemon by opening its context." )
            daemon_context.open()

            logging.info( "Calling read_store_readings...." )
            read_store_readings()

            logging.debug( "Closing the daemon context." )
            daemon_context.close()

        else:
            logging.info( "Server running on Windows system ..." )
            read_store_readings()

    return


if __name__ == "__main__":
    run()
