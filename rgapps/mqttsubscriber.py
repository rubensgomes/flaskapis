"""rgapps.mqttsubscriber MQTT background daemon subscriber

This program is an MQTT subscriber that subscribes to the sensor TOPIC
destination defined in the configuration file.
"""
import logging
import platform
import signal
import sys
import time

from rgapps.config import ini_config
from rgapps.mqtt.mqtt import MQTTSubscriber
from rgapps.utils.utility import write_to_file


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

def subscribe_sensor_data():
    """ Function used to subscribe to topic destination where sensor readings
    are being published.
    """

    # MQTT client publisher
    mqtt_subscriber = MQTTSubscriber()

    sleep_timeout = ini_config.getint("Sensor", "SENSOR_SLEEP_TIME")

    # start daemon forever loop
    while True:

        try:
            # read and publish sensor reading to topic in MQTT server
            logging.debug("subscribing to sensor TOPIC destination...")

            mqtt_subscriber.subscribe_temperature()

        except (Exception) as err:
            sys.stderr.write(str(err))
            logging.exception("Error subscribing to sensor data. [{0}]"
                               .format(err))

        except:  # catch *all* other exceptions
            err = sys.exc_info()[0]
            logging.exception("Error occurred in mqtt daemon: [{0}]"
                               .format(err))

            write_to_file("<p>Error in mqttsubscriber daemon: [{0}]</p>"
                          .format(err), sys.stderr)

        time.sleep(sleep_timeout)

    return

def program_cleanup(signum, frame):
    """ daemon cleanup code run on Linux when handling SIGTERM (15) signal
    """
    logging.info("Program terminating with signum [{0}] under Linux."
                  .format(signum))
    exit(0)


def run():
    """ daemon run function.

    This function should be called to start the system.
    """

    from rgapps.utils.utility import get_log_file_handles
    logger_fds = get_log_file_handles(logging.getLogger())
    logging.debug("Logger file handles fileno [{0}]".format(logger_fds))

    system = platform.system()

    if system == "Linux":
        logging.info("Server running on Linux.")

        pid_file = ini_config.getboolean("Sensor", "SENSOR_PID_FILE")
        working_dir = ini_config.getboolean("Logging", "WORKING_DIR")

        logging.debug("Instantiating daemon with pid_file [{0}] "
                       "and working_dir [{1}]"
                       .format(pid_file, working_dir))

        import daemon.pidfile

        daemon_context = daemon.DaemonContext(
            working_directory=working_dir,
            umask=0o002,
            pidfile=daemon.pidfile.PIDLockFile(pid_file))

        logging.debug("Setting up daemon signal map")
        daemon_context.signal_map = { signal.SIGTERM: program_cleanup }
        logging.debug("daemon signal map has been setup")

        if (logger_fds):
            logging.debug("setting files_preserve for the log file "
                           "descriptor [{0}]".format(logger_fds))
            daemon_context.files_preserve = logger_fds

        logging.debug("Starting daemon by opening its context.")
        daemon_context.open()

        logging.info("Calling subscribe_sensor_data....")
        subscribe_sensor_data()

        logging.debug("Closing the daemon context.")
        daemon_context.close()

    else:
        logging.info("Server running on Windows system ...")
        subscribe_sensor_data()


if __name__ == "__main__":
    run()
