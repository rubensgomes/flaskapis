"""mqttdaemon MQTT background daemon job

This program collects data from sensors periodically and publishes a message
with the data collected to topic in a MQTT server.
"""
import platform
import signal
import sys
import time

from flask import Flask
from werkzeug.exceptions import BadRequest


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"



# app: Flask application object
app = Flask( __name__,
            instance_path=FLASKAPIS_INSTANCE_PATH,
            instance_relative_config=True )

app.config.from_pyfile( DEFAULT_INI_FILE, silent=False )


def read_publish_sensor_data():
    """ Function used to read sensor data and publish the readings to a topic
    served by an MQTT server.
    """

    # MQTT client publisher
    mqtt_publisher = MQTTPublisher()

    sensor_serial = app.config["SENSOR_TEMPERATURE_SERIAL"]
    sleep_timeout = app.config["SENSOR_SLEEP_TIME"]

    with app.app_context():

        # start daemon forever loop
        while True:

            try:
                # read and publish sensor reading to topic in MQTT server
                app.logger.debug( "publishing sensor serial [{0}] data"
                                 .format( sensor_serial ) )

                mqtt_publisher.publish_temperature( sensor_serial )

            except ( BadRequest ) as err:  # e.g., sensor serial not provided
                sys.stderr.write( str( err ) )
                app.logger.exception( "Sensor serial not provided. [{0}]"
                                     .format( err ) )

            except ( Exception ) as err:
                sys.stderr.write( str( err ) )
                app.logger.exception( "Error reading/publishing sensor data. [{0}]"
                                     .format( err ) )

            except:  # catch *all* other exceptions
                err = sys.exc_info()[0]
                app.logger.exception( "Error occurred in mqtt daemon: [{0}]"
                                     .format( err ) )

                write_to_file( "<p>Error in runsensor daemon: [{0}]</p>"
                              .format( err ), sys.stderr )


            time.sleep( sleep_timeout )

    return

def program_cleanup( signum, frame ):
    """ daemon cleanup code run on Linux when handling SIGTERM (15) signal
    """
    with app.app_context():
        app.logger.info( "Program terminating with signum [{0}] under Linux."
                        .format( signum ) )
    exit( 0 )


def run():
    """ daemon run function.

    This function should be called to start the system.
    """

    with app.app_context():

        set_up_environment()
        app.logger.debug( "Environment has been initialized." )
        app.logger.info( "Starting application ..." )

        from flaskapis.utils.utility import get_log_file_handles
        logger_fds = get_log_file_handles( app.logger )
        app.logger.debug( "Logger file handles fileno [{0}]".format( logger_fds ) )

        system = platform.system()

        if system == "Linux":
            app.logger.info( "Server running on Linux." )

            pid_file = app.config["SENSOR_PID_FILE"]
            working_dir = app.config["WORKING_DIR"]

            app.logger.debug( "Instantiating daemon with pid_file [{0}] "
                             "and working_dir [{1}]"
                             .format( pid_file, working_dir ) )

            import daemon.pidfile

            daemon_context = daemon.DaemonContext( 
                working_directory=working_dir,
                umask=0o002,
                pidfile=daemon.pidfile.PIDLockFile( pid_file )
                )

            app.logger.debug( "Setting up daemon signal map" )
            daemon_context.signal_map = {
                                         signal.SIGTERM: program_cleanup
                                         }
            app.logger.debug( "daemon signal map has been setup" )

            if ( logger_fds ):
                app.logger.debug( "setting files_preserve for the log file "
                                 "descriptor [{0}]".format( logger_fds ) )
                daemon_context.files_preserve = logger_fds

            app.logger.debug( "Starting daemon by opening its context." )
            daemon_context.open()

            app.logger.info( "Calling read_store_readings...." )
            read_publish_sensor_data()

            app.logger.debug( "Closing the daemon context." )
            daemon_context.close()

        else:
            app.logger.info( "Server running on Windows system ..." )
            read_publish_sensor_data()


if __name__ == "__main__":
    run()
