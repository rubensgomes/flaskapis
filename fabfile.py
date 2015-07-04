"""Fabric file

This file is used to do remote deployment of the flaskapis application
and the flaskapis swagger-doc files to a remote Linux server.  It was
written to run from a Windows DOS prompt, and it should run from the
ROOT folder of the flaskapis application.

"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

from fabric.api import cd, local, run, put, task

REMOTE_HOME = r"/home/wsgi"
REMOTE_FLASKAPIS_INSTALLDIR = r"%s/flaskapis" % REMOTE_HOME
# REMOTE_FLASKAPIS_INSTALLDIR = r"%s/dev" % REMOTE_HOME
REMOTE_VIRTUALENV = r"%s/venv/" % REMOTE_FLASKAPIS_INSTALLDIR

@task
def clean():
    """Used to clean previous build.
    """
    print("---cleaning local build")
    local("python setup.py clean")
    local("IF EXIST python3.2m.exe.stackdump DEL /Q python3.2m.exe.stackdump")
    local("IF EXIST ez_setup.pyc DEL /Q ez_setup.pyc")
    local("IF EXIST fabfile.pyc DEL /Q fabfile.pyc")
    local("IF EXIST dist RMDIR /S /Q dist")
    local("IF EXIST build RMDIR /S /Q build")
    local("IF EXIST __pycache__ RMDIR /S /Q __pycache__")
    local("IF EXIST flaskapis\__pycache__ RMDIR /S /Q flaskapis\__pycache__")
    local("IF EXIST flaskapis.egg-info RMDIR /S /Q flaskapis.egg-info")


@task
def pack():
    """Used to create a python installation distribution package file.
    """
    print("---creating a new tarball file")
    clean()
    local('python setup.py sdist --formats=gztar', capture=False)


@task
def copy_app():
    """Used to copy python installation installation package file to
    remote server.
    """
    pack()
    print("---copying application files to remote server")
    # figure out the release name and version
    dist = local("python setup.py --fullname", capture=True).strip()
    # upload the source tarball to the temporary folder on the server
    run("if [ -f /tmp/flaskapis.tar.gz ]; then rm -f /tmp/flaskapis.tar.gz; fi")
    run("if [ -d /tmp/flaskapis/dist ]; then rm -fr /tmp/flaskapis/dist; fi")
    put("dist/{0}.tar.gz".format(dist), "/tmp/flaskapis.tar.gz")
    # create a place where we can unzip the tarball, then enter that directory
    # and unzip it
    run("if [ ! -d /tmp/flaskapis/dist ]; then mkdir -p /tmp/flaskapis/dist; fi")
    run("cd /tmp/flaskapis/dist; tar xzf /tmp/flaskapis.tar.gz")


@task
def deploy_flaskapis():
    """Used to deploy the FLASKAPIS RESTFul APIs to remote server.
    """
    copy_app()
    print("---installing application in the flaskapis remote server")
    # figure out the release name and version
    fullname = local("python setup.py --fullname", capture=True)
    with cd("{0}".format(REMOTE_HOME)):
        run("if [ -d w1thermsensor ]; then rm -fr w1thermsensor; fi")
        run("git clone https://github.com/timofurrer/w1thermsensor.git")
        run(("cd w1thermsensor; {0}/bin/python -v setup.py install")
            .format(REMOTE_VIRTUALENV))
    with cd("/tmp/flaskapis/dist/{0}".format(fullname)):
        print("---setup package with virtual environment's python interpreter")
        run("{0}/bin/pip install -v --upgrade .".format(REMOTE_VIRTUALENV))
        run("if [ ! -f {0}/application.cfg ]; then "
            "cp -v application.cfg {0};"
            "fi".format(REMOTE_FLASKAPIS_INSTALLDIR))
        run("cp -v flaskapis.wsgi {0}".format(REMOTE_FLASKAPIS_INSTALLDIR))
        run("if [ ! -f {0}/flaskapis.db ]; then "
            "sqlite3 {0}/flaskapis.db < db/db_schema.sql;"
            "sqlite3 {0}/flaskapis.db < db/db_data.sql;"
            "fi".format(REMOTE_FLASKAPIS_INSTALLDIR))
    # now that all is set up, delete the folder again
    run("rm -fr /tmp/flaskapis/dist; rm -f /tmp/flaskapis.tar.gz")
    run("rm -fr /tmp/flaskapis")
    # run 2to3 if needed
    with cd("{0}/flaskapis".format(REMOTE_HOME)):
        print("---running python 2to3 if needed.")
        run("source venv/bin/activate; "
            "python --version | grep -n -i \"python 3\"; "
            "if [ ${?} -eq 0 ]; then "
            "2to3 -v -W venv/lib/python3.4/site-packages/flaskapis; "
            "2to3 -v -W venv/lib/python3.4/site-packages/validate_email.py; "
            "fi; "
            "deactivate")
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    run("touch {0}/flaskapis.wsgi".format(REMOTE_FLASKAPIS_INSTALLDIR))


@task
def deploy_sensorserver():
    """Used to deploy the sensorserver daemon to remote server.
    """
    copy_app()
    print("------installing sensorserver in the sensorserver remote server")
    # figure out the release name and version
    fullname = local("python setup.py --fullname", capture=True)
    with cd("/tmp/flaskapis/dist/{0}".format(fullname)):
        run("if [ ! -f /home/wsgi/sensorserver/application.cfg ]; then "
            "cp -v application.cfg /home/wsgi/sensorserver;"
            "fi")
        # setup the package with our virtual environment's python interpreter
        run("/home/wsgi/sensorserver/venv/bin/pip install -v --upgrade .")
        run("cp sensorserver.py /home/wsgi/sensorserver")
    # now that all is set up, delete the folder again
    run("rm -fr /tmp/flaskapis/dist; rm -f /tmp/flaskapis.tar.gz")
    run("rm -fr /tmp/flaskapis")


@task
def deploy_site():
    """Used to the FLASKAPIs swagger REST API documentation to remote server.
    """
    print("---deploying the swagger-doc site files to remote server")
    run("if [ ! -d /var/www/restportal ]; then mkdir -p /var/www/restportal; fi")
    put("misc/swagger-doc", "/var/www/restportal")
