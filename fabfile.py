"""Fabric file

This file is used to do builds and remote deployment of the application
and the the swagger-doc files to a remote Linux server.  It was
written to run from a Windows DOS prompt, and it should run from the
ROOT folder of the application.


ATTENTION: This code should be run from a DOS prompt.

To clean:
fab clean

To create package:
fab pack

To deploy:
fab -u <user> -p <pwd> -H <server>:<port> deploy_<..>
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

from fabric.api import cd, local, run, put, task

REMOTE_HOME = r"/home/wsgi"
RESTAPIS_INSTALLDIR = r"%s/flaskapis" % REMOTE_HOME
SENSORAPP_INSTALLDIR = r"%s/sensorserver" % REMOTE_HOME
REMOTE_VIRTUALENV = r"%s/venv/" % RESTAPIS_INSTALLDIR

@task
def clean():
    """Used to clean previous build.
    """
    print( "---cleaning local build" )
    local( "python setup.py clean", capture=False )
    local( "IF EXIST dist RMDIR /S /Q dist", capture=False )
    local( "IF EXIST build RMDIR /S /Q build", capture=False )
    local( "IF EXIST flaskapis.egg-info RMDIR /S /Q flaskapis.egg-info", 
           capture=False )
#    local( "FOR /R %f IN (*.pyc) DO (DEL /S /Q %f)", capture=False )
#    local( "FOR /R %f IN (*.stackdump) DO (DEL /S /Q %f)", capture=False )
#    local( "FOR /D /R %d IN (__pycache__*) DO (RMDIR /S /Q %d)", capture=False )

@task
def pack():
    """Used to create a python installation distribution package file.
    """
    print( "---creating a new tarball file" )
    clean()
    local( 'python setup.py sdist --formats=gztar', capture=False )


@task
def copy_expand_dist():
    """Used to copy/expand python dist package file to remote server.
    """
    pack()
    print( "---copying package file to remote server" )
    # figure out the release name and version
    dist = local( "python setup.py --fullname", capture=True ).strip()
    # upload the source tarball to the temporary folder on the server
    run( "if [ -f /tmp/flaskapis.tar.gz ]; then rm -f /tmp/flaskapis.tar.gz; fi" )
    run( "if [ -d /tmp/flaskapis/dist ]; then rm -fr /tmp/flaskapis/dist; fi" )
    put( "dist/{0}.tar.gz".format( dist ), "/tmp/flaskapis.tar.gz" )
    # create a place where we can unzip the tarball, then enter that directory
    # and unzip it
    run( "if [ ! -d /tmp/flaskapis/dist ]; then mkdir -p /tmp/flaskapis/dist; fi" )
    run( "cd /tmp/flaskapis/dist; tar xzf /tmp/flaskapis.tar.gz" )


@task
def deploy_rest_apis():
    """Used to deploy the RESTFul APIs to remote server.
    """
    copy_expand_dist()
    print( "---installing application in the remote server" )
    # figure out the release name and version
    fullname = local( "python setup.py --fullname", capture=True )
    with cd( "{0}".format( REMOTE_HOME ) ):
        print( "---installing w1thermsensor" )
        run( "if [ -d w1thermsensor ]; then rm -fr w1thermsensor; fi" )
        run( "git clone https://github.com/timofurrer/w1thermsensor.git" )
        run( ( "cd w1thermsensor; {0}/bin/python -v setup.py install" )
            .format( REMOTE_VIRTUALENV ) )
    with cd( "/tmp/flaskapis/dist/{0}".format( fullname ) ):
        print( "---use pip to install package in virtual environment" )
        run( "{0}/bin/pip install -v --upgrade .".format( REMOTE_VIRTUALENV ) )
        run( "if [ ! -f {0}/application.ini ]; then "
            "cp -v application.ini {0};"
            "fi".format( RESTAPIS_INSTALLDIR ) )
        run( "cp -v flaskapis.wsgi {0}".format( RESTAPIS_INSTALLDIR ) )
        run( "if [ ! -f {0}/flaskapis.db ]; then "
            "sqlite3 {0}/flaskapis.db < db/db_schema.sql;"
            "sqlite3 {0}/flaskapis.db < db/db_data.sql;"
            "fi".format( RESTAPIS_INSTALLDIR ) )
    # now that all is set up, delete the folder again
    run( "rm -fr /tmp/flaskapis/dist; rm -f /tmp/flaskapis.tar.gz" )
    run( "rm -fr /tmp/flaskapis" )
    # run 2to3 if needed
    with cd( RESTAPIS_INSTALLDIR ):
        print( "---running python 2to3 if needed." )
        run( "source venv/bin/activate; "
            "python --version | grep -n -i \"python 3\"; "
            "if [ ${?} -eq 0 ]; then "
            "2to3 -v -W venv/lib/python3.4/site-packages/flaskapis; "
            "2to3 -v -W venv/lib/python3.4/site-packages/validate_email.py; "
            "fi; "
            "deactivate" )
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    run( "touch {0}/flaskapis.wsgi".format( RESTAPIS_INSTALLDIR ) )


@task
def deploy_sensorapp():
    """Used to deploy the sensorapp daemon to remote server.
    """
    copy_expand_dist()
    print( "------installing sensorapp in the remote server" )
    # figure out the release name and version
    fullname = local( "python setup.py --fullname", capture=True )
    with cd( "/tmp/flaskapis/dist/{0}".format( fullname ) ):
        run( "if [ ! -f {0}/application.ini ]; then "
            "cp -v application.ini {0};"
            "fi".format( SENSORAPP_INSTALLDIR ) )
        # setup the package with our virtual environment's python interpreter
        run( "{0}/venv/bin/pip install -v --upgrade ."
             .format( SENSORAPP_INSTALLDIR ) )
        run( "cp -v rgapps/sensorapp.py {0}".format( SENSORAPP_INSTALLDIR ) )
    # now that all is set up, delete the folder again
    run( "rm -fr /tmp/flaskapis/dist; rm -f /tmp/flaskapis.tar.gz" )
    run( "rm -fr /tmp/flaskapis" )
    # run 2to3 if needed
    with cd( SENSORAPP_INSTALLDIR ):
        print( "---running python 2to3 if needed." )
        run( "source venv/bin/activate; "
            "python --version | grep -n -i \"python 3\"; "
            "if [ ${?} -eq 0 ]; then "
            "2to3 -v -W venv/lib/python3.4/site-packages/flaskapis; "
            "2to3 -v -W venv/lib/python3.4/site-packages/validate_email.py; "
            "fi; "
            "deactivate" )


@task
def deploy_rest_doc():
    """Used to deploy swagger REST API documentation to remote server.
    """
    print( "---deploying the swagger-doc site files to remote server" )
    run( "if [ ! -d /var/www/restportal ]; then mkdir -p /var/www/restportal; fi" )
    put( "misc/swagger-doc", "/var/www/restportal" )
