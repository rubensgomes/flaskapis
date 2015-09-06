""" Python setuptools setup.py file for the flaskapis RESTful APIs

flaskapis is a set of REST APIs implemented using Python using the
flask-restful library.
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup

setup( 
    name="FlaskAPIs",
    ### ADD VERSION BELOW TO README.rst FILE !!!
    version="2015.9.dev2",
    author="Rubens S. Gomes",
    author_email="rubens.s.gomes@gmail.com",
    contact_email="rubens.s.gomes@gmail.com",
    maintainer="Rubens S. Gomes",
    maintainer_email="rubens.s.gomes@gmail.com",
    url="http://restportal.com/",
    description="The RGApps Python project",
    long_description=__doc__,
    platforms=["Linux", "Windows"],
    packages=["rgapps"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
      "arrow>=0.5.4",
      "enum34>=1.0.4",
      "nose>=1.3.4",
      "requests>=2.6.0",
      "sure>=1.2.9",
      "validate_email>=1.2",
      "Flask>=0.10.1",
      "Flask-RESTful>=0.3.2",
      "Pint>=0.6",
      "python-daemon>=2.0.5",
      "w1thermsensor>=0.2.1",
      "paho-mqtt>=1.1",
      "beautifulsoup4>=4.4.0",
      "RPi.GPIO>=0.5.11",
      "six>=1.9.0",
      "pymongo>=3.0.3"
    ],
    keywords="flask flask-restful REST RESTful APIs"
 )
