==============================================
Build and Deployment Installation Instructions
==============================================

To Clean a Previous Build
-------------------------

To clean a previous build, run the following command from the root
of the *rgapps* project folder in a Windows DOS shell prompt::

    fab clean

To Build a Python Dist Package File Locally
-------------------------------------------

To create a python dist, run the following command from the root
of the *rgapps* project folder in a Windows DOS shell prompt::

    fab pack

To Copy/Expand Python Dist Package File to a Remote Host
--------------------------------------------------------

To copy and expand the python dist to a remote server, run the
following command from the root of the *rgapps* project folder in a
Windows DOS shell prompt::

    fab copy_expand_dist

To Deploy the REST APIs to a Remote Server Host
-----------------------------------------------

To deploy a python dist to a remote server, run the following command from
the root of the *rgapps* project folder in a Windows DOS shell prompt::

    fab -u <username> -p <password> -H <host:port> deploy_rest_apis

**NOTICE** The username should be the previously configured "wsgi" on that
remote server.

To Deploy the sensorapp to a Remote Server Host
-----------------------------------------------

To deploy the sensorapp to a remote server, run the following command from
the root of the *rgapps* project folder in a Windows DOS shell prompt::

    fab -u <username> -p <password> -H <host:port> deploy_sensorapp


To Deploy the REST API documentation to a Remote Server Host
------------------------------------------------------------

To deploy the *rgapps* REST swagger-doc site files to a remote server,
run the following command from the root of the *rgapps* project folder in
a Windows DOS shell prompt::

    fab -u <username> -p <password> -H <host:port> deploy_rest_doc
