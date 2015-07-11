"""sensorserver background daemon job

This program collects data from sensors periodically and store the
readings in the database.
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"


import platform
import signal
import sys
import time

from flask import Flask
import requests
from requests.exceptions import (ConnectionError, Timeout,
                                 RequestException, HTTPError)

from flaskapis.config import set_up_environment
from flaskapis.constants import DATA_KEY, SENSOR_KEY, \
    SENSORSERVER_INSTANCE_PATH, DEFAULT_INI_FILE
from flaskapis.db.sensor import SensorDb
from flaskapis.utils.utility import write_to_file, EMail


# app: Flask application object
app = Flask(__name__,
            instance_path=SENSORSERVER_INSTANCE_PATH,
            instance_relative_config=True)

app.config.from_pyfile(DEFAULT_INI_FILE, silent=False)


def read_store_readings():
    """ Function used to read and store sensor readings
    """

    # error flag used to send email only once if error occurs.
    error_flag = False

    # mail object used when sending email
    mail = EMail()

    # sensor db object used when reading/storing into database
    sensorDb = SensorDb()

    headers = {'content-type': 'application/json'}
    rest_url = (app.config["SENSOR_TEMPERATURE_URL"] + "/" + 
                app.config["SENSOR_TEMPERATURE_SERIAL"])
    rest_user = app.config["SENSOR_REST_API_USERNAME"]
    rest_pw = app.config["SENSOR_REST_API_PASSWORD"]
    req_timeout = app.config["SENSOR_REQUEST_TIMEOUT"]
    recipient = app.config["RECIPIENT_EMAIL"]
    sleep_timeout = app.config["SENSOR_SLEEP_TIME"]

    with app.app_context():

        # start daemon forever loop
        while True:

            try:
                # collect data from sensor using RESTFul API
                app.logger.debug("Sending request to [{0}] with user [{1}]"
                                 .format(rest_url, rest_user))

                r = requests.get(rest_url,
                                 verify=False,
                                 auth=(rest_user, rest_pw),
                                 headers=headers,
                                 timeout=req_timeout)

                # if code gets here no exception has occurred. reset flag.
                error_flag = False

                if (r.status_code != 200):
                    app.logger.error("Response status code [{0}] : [{1}]"
                                     .format(r.status_code, r.text))
                else:
                    output = r.json()
                    sensor = output[SENSOR_KEY]
                    readings = output[DATA_KEY]

                    app.logger.debug("Adding sensor record with unit [{0}], "
                                      "value [{1}], utc [{2}], serial [{3}] to "
                                      "database."
                                     .format(readings["unit"],
                                             readings["value"],
                                             readings["utc"],
                                             sensor["serial"]))

                    sensorDb.add_measurement(readings["unit"],
                                            readings["value"],
                                            readings["utc"],
                                            sensor["serial"])

            # python 3.4: ConnectionRefusedError
            except (ConnectionError, Timeout) as err:  # e.g., server is down.
                sys.stderr.write(str(err))

                app.logger.exception("Connection Error with URL [{0}], "
                                     "user [{1}] in runserver daemon: [{2}]"
                                     .format(rest_url, rest_user, err))

                if not error_flag :  # only send email once.
                    subject = "sensorserver: Connection/Timeout Error"
                    app.logger.info("Sending email to [{0}] with subject [{1}]"
                                    .format(recipient, subject))
                    message = ("Connection/Timeout Error to URL [{0}]: [{1}]"
                               .format(rest_url, err))
                    try:
                        mail.send_email(recipient, subject, message)
                        app.logger.info(
                            "email to [{0}] with subject [{1}] was sent."
                            .format(recipient, subject)
                            )
                    except Exception as mail_err:
                        app.logger.error("Error [{0}] sending email."
                                         .format(mail_err))

                error_flag = True

            except (HTTPError, RequestException) as err:
                sys.stderr.write(str(err))

                app.logger.exception("HTTP/Request Error to URL [{0}] in "
                                      "runserver daemon: [{1}]"
                                     .format(rest_url, err))

                if not error_flag :  # only send email once.
                    subject = "sensorserver: HTTP Error"
                    app.logger.info("Sending email to [{0}] with subject [{1}]"
                                    .format(recipient, subject))
                    message = ("HTTP/Request to URL [{0}] Error: [{1}]"
                               .format(rest_url, err))

                    try:
                        mail.send_email(recipient, subject, message)
                        app.logger.info(
                            "email to [{0}] with subject [{1}] was sent."
                            .format(recipient, subject)
                            )
                    except Exception as mail_err:
                        app.logger.error("Error [{0}] sending email."
                                         .format(mail_err))

                error_flag = True

            except (EnvironmentError, Exception) as err:
                sys.stderr.write(str(err))

                app.logger.exception("Error in runserver daemon: [{0}]"
                                     .format(err))

                if not error_flag :  # only send email once.
                    subject = "sensorserver: Environment Error"
                    app.logger.info("Sending email to [{0}] with subject [{1}]"
                                    .format(recipient, subject))
                    message = "EXITING APPLICATION. Error: [{0}]".format(err)

                    try:
                        mail.send_email(recipient, subject, message)
                        app.logger.info(
                            "email to [{0}] with subject [{1}] was sent."
                            .format(recipient, subject)
                            )
                    except Exception as mail_err:
                        app.logger.error("Error [{0}] sending email."
                                         .format(mail_err))

                error_flag = True

            except:  # catch *all* other exceptions
                err = sys.exc_info()[0]
                app.logger.exception("Error occurred in runserver daemon: [{0}]"
                                     .format(err))

                write_to_file("<p>Error in runsensor daemon: [{0}]</p>"
                              .format(err), sys.stderr)
                exit(1)


            time.sleep(sleep_timeout)

    return

def program_cleanup(signum, frame):
    """ daemon cleanup code run on Linux when handling SIGTERM (15) signal
    """
    with app.app_context():
        app.logger.info("Program terminating with signum [{0}] under Linux."
                        .format(signum))
    exit(0)


def run():
    """ daemon run function.

    This function should be called to start the system.
    """

    with app.app_context():

        set_up_environment()
        app.logger.debug("Environment has been initialized.")
        app.logger.info("Starting application ...")

        from flaskapis.utils.utility import get_log_file_handles
        logger_fds = get_log_file_handles(app.logger)
        app.logger.debug("Logger file handles fileno [{0}]".format(logger_fds))

        system = platform.system()

        if system == "Linux":
            app.logger.info("Server running on Linux.")

            pid_file = app.config["SENSOR_PID_FILE"]
            working_dir = app.config["WORKING_DIR"]

            app.logger.debug("Instantiating daemon with pid_file [{0}] "
                             "and working_dir [{1}]"
                             .format(pid_file, working_dir))

            import daemon.pidfile

            daemon_context = daemon.DaemonContext(
                working_directory=working_dir,
                umask=0o002,
                pidfile=daemon.pidfile.PIDLockFile(pid_file)
                )

            app.logger.debug("Setting up daemon signal map")
            daemon_context.signal_map = {
                                         signal.SIGTERM: program_cleanup
                                         }
            app.logger.debug("daemon signal map has been setup")

            if (logger_fds):
                app.logger.debug("setting files_preserve for the log file "
                                 "descriptor [{0}]".format(logger_fds))
                daemon_context.files_preserve = logger_fds

            app.logger.debug("Starting daemon by opening its context.")
            daemon_context.open()

            app.logger.info("Calling read_store_readings....")
            read_store_readings()

            app.logger.debug("Closing the daemon context.")
            daemon_context.close()

        else:
            app.logger.info("Server running on Windows system ...")
            read_store_readings()


if __name__ == "__main__":
    run()
