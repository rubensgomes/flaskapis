"""rgapps.http.errors module

This is where all the HTTP error handlers are defined.
"""
import cgi
from collections import OrderedDict
import csv
import io
import logging
import re
from xml.sax import saxutils

from flask import request, jsonify, Response
from flask.ext.restful import Api
from pint import DimensionalityError

from rgapps.utils.constants import STATUS_KEY, STATUS_ERROR
from rgapps.utils.utility import is_blank, get_error_description


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["ErrorResponse", "FlaskRESTfulAPI"]




class FlaskRESTfulAPI( Api ):
    """
    Subclass of the flask_restful API class used in order to
    override the handle_error method.
    """

    def handle_error( self, error ):
        """
        Overrides flask-restful error handler

        Parameters
        ----------
        error:  Exception object (required)
            the exception error object.

        Returns
        -------
            this method which overrides handle_error in flask-restful API.
        """
        logging.debug( "inside handle_error" )

        if isinstance( error, ( DimensionalityError, DimensionalityError ) ):
            logging.debug( "handling DimensionalityError or DimensionalityError" )
            return self.pint_bad_request( error )

        elif isinstance( error, ( TypeError, ValueError ) ):
            logging.debug( "handling TypeError or ValueError" )
            return self.handle_internal_server_error( error )

        else:
            # if code not found in error, default to 500
            code = 500
            if hasattr( error, 'code' ):
                code = getattr( error, 'code' )

            if code == 400:
                return self.bad_request( error )
            elif code == 401:
                return self.handle_not_authorized( error )
            elif code == 402 or code == 403 or code == 407:
                return self.handle_not_expected( error )
            elif code == 404:
                return self.handle_not_found( error )
            elif code == 405:
                return self.method_not_allowed( error )
            elif code == 406:
                return self.handle_not_acceptable( error )
            elif code == 408:
                return self.handle_request_timeout( error )
            elif code >= 500:
                return self.handle_internal_server_error( error )
            else:
                return self.handle_not_acceptable( error )

        return super( FlaskRESTfulAPI, self ).handle_error( error )


    def pint_bad_request( self, error ):
        """
        This method handles an exception error when the HTTP request
        could not be served due to a malformed request (e.g., some
        parameters are not valid).

        Parameters
        ----------
        error:  Exception object (required)
            the exception error object.

        Returns
        -------
            an HTTP response object with appropriate error message.
        """
        logging.debug( "inside pint_bad_request" )

        code = ""

        if hasattr( error, 'code' ):
            code = getattr( error, 'code' )

        logging.debug( "Handling a status_code [{0}] error [{1}]"
                      .format( code, error ) )

        response = ErrorResponse.get_response( 400,
                                              str( error ),
                                              "application/json" )
        return response


    def bad_request( self, error ):
        """
        This method handles an exception error when the HTTP request
        could not be served due to a malformed request (e.g., some
        parameters are not valid).

        Parameters
        ----------
        error:  Exception object (required)
            the exception error object.

        Returns
        -------
            an HTTP response object with appropriate error message.

        """
        logging.debug( "inside bad_request" )

        code = ""

        if hasattr( error, 'code' ):
            code = getattr( error, 'code' )

        logging.debug( "Handling a status_code [{0}] error [{1}]"
                      .format( code, error ) )

        # if a description was found on the error, use that one instead
        description = get_error_description( error )
        if is_blank( description ):
            description = "Bad URL [{0}] request".format( request.url )

        response = ErrorResponse.get_response( 400,
                                              description,
                                              "application/json" )
        return response


    def handle_not_authorized( self, error ):
        """
        This method handles an exception error when the requested URL is
        not authenticated.

        Parameters
        ----------
        error:  Exception object (required)
            the exception error object.

        Returns
        -------
            an HTTP response object with appropriate error message.
        """
        logging.debug( "inside handle_not_authorized" )

        code = ""

        if hasattr( error, 'code' ):
            code = getattr( error, 'code' )

        logging.debug( "Handling a status_code [{0}] error [{1}]"
                      .format( code, error ) )

        # if a description was found on the error, use that one instead
        description = get_error_description( error )
        if is_blank( description ):
            description = "URL [{0}] request not authorized".format( request.url )

        response = ErrorResponse.get_response( 401,
                                              description,
                                              "application/json" )
        response.headers["WWW-Authenticate"] = 'Basic realm = "IoT Gateway"'
        return response


    def handle_request_timeout( self, error ):
        """
        This method handles an exception error when the request times out.

        Parameters
        ----------
        error:  Exception object (required)
            the exception error object.

        Returns
        -------
            an HTTP response object with appropriate error message.
        """
        logging.debug( "inside handle_request_timeout" )

        code = ""

        if hasattr( error, 'code' ):
            code = getattr( error, 'code' )

        logging.debug( "Handling a status_code [{0}] error [{1}]"
                      .format( code, error ) )

        # if a description was found on the error, use that one instead
        description = get_error_description( error )
        if is_blank( description ):
            description = "URL [{0}] request timed out".format( request.url )

        response = ErrorResponse.get_response( 408,
                                              description,
                                              "application/json" )
        response.headers["WWW-Authenticate"] = 'Basic realm = "IoT Gateway"'
        return response


    def handle_not_expected( self, error ):
        """
        This method handles an exception error for an HTTP status code that
        is currently not supported, and it was not expected.

        Parameters
        ----------
        error:  Exception object (required)
            the exception error object.

        Returns
        -------
            an HTTP response object with appropriate error message.
        """
        logging.debug( "inside handle_not_expected" )

        code = ""

        if hasattr( error, 'code' ):
            code = getattr( error, 'code' )

        logging.debug( "Handling a status_code [{0}] error [{1}]"
                      .format( code, error ) )

        # if a description was found on the error, use that one instead
        description = get_error_description( error )
        if is_blank( description ):
            description = ( "URL [{0}] request generate a not expected status"
                            .format( request.url ) )

        response = ErrorResponse.get_response( 401,
                                              description,
                                              "application/json" )
        response.headers["WWW-Authenticate"] = 'Basic realm = "IoT Gateway"'
        return response


    def handle_not_found( self, error ):
        """
        This method handles an exception error when the requested URL
        resource was not found on the server.

        Parameters
        ----------
        error:  Exception object (required)
            the exception error object.

        Returns
        -------
            an HTTP response object with appropriate error message.

        """
        logging.debug( "inside handle_not_found" )

        code = ""

        if hasattr( error, 'code' ):
            code = getattr( error, 'code' )

        logging.debug( "Handling a status_code [{0}] error [{1}]"
                                 .format( code, error ) )

        url_not_found = request.url
        logging.debug( "Handling a URL [{0}] not found error [{1}]"
                                 .format( url_not_found, error ) )

        # if a description was found on the error, use that one instead
        description = get_error_description( error )
        if is_blank( description ):
            description = ( "Requested resource identified by [{0}] not found."
                            .format( url_not_found ) )

        response = ErrorResponse.get_response( 404,
                                              description,
                                              "application/json" )
        return response


    def method_not_allowed( self, error ):
        """
        This method handles an exception error when the HTTP method
        sent is not supported.

        Parameters
        ----------
        error:  Exception object (required)
            the exception error object.

        Returns
        -------
            an HTTP response object with appropriate error message.
        """
        logging.debug( "inside method_not_allowed" )

        code = ""

        if hasattr( error, 'code' ):
            code = getattr( error, 'code' )

        logging.debug( "Handling a status_code [{0}] error [{1}]"
                                 .format( code, error ) )

        method = request.method

        # if a description was found on the error, use that one instead
        description = get_error_description( error )
        if is_blank( description ):
            description = "The HTTP method [{0}] is not supported.".format( method )

        response = ErrorResponse.get_response( 405,
                                              description,
                                              "application/json" )
        return response


    def handle_not_acceptable( self, error ):
        """
        This method handles an exception error when none of the media
        types defined in the incoming HTTP Accept header is supported
        by this REST API.

        Parameters
        ----------
        error:  Exception object (required)
            the exception error object.

        Returns
        -------
            an HTTP response object with appropriate error message.
        """
        logging.debug( "inside handle_not_acceptable" )

        code = ""

        if hasattr( error, 'code' ):
            code = getattr( error, 'code' )

        logging.debug( "Handling a status_code [{0}] error [{1}]"
                       .format( code, error ) )

        mimeType = request.accept_mimetypes.best
        logging.debug( "Handling a 406 error [{0}].  "
                                 "The best mime type is [{1}]"
                                 .format( error, mimeType ) )
        accept = request.headers['Accept']

        # if a description was found on the error, use that one instead
        description = get_error_description( error )
        if is_blank( description ):
            description = ( "Requested MIME types [{0}] not supported."
                            .format( accept ) )

        response = ErrorResponse.get_response( 406,
                                              description,
                                              mimeType )
        return response


    def handle_internal_server_error( self, error ):
        """
        This method handles an internal server exception error.

        Parameters
        ----------
        error:  Exception object (required)
            the exception error object.

        Returns
        -------
            an HTTP response object with appropriate error message.
        """
        logging.debug( "inside handle_internal_server_error" )

        code = 500

        if hasattr( error, 'code' ):
            code = getattr( error, 'code' )

        logging.debug( "Handling a status_code [{0}] error [{1}]"
                       .format( code, error ) )

        # if a description was found on the error, use that one instead
        description = get_error_description( error )
        if is_blank( description ):
            description = "An internal server error occurred"

        if isinstance( error, Exception ):
            logging.exception( error )

        response = ErrorResponse.get_response( code, description,
                                               "application/json" )
        return response


class ErrorResponse:
    """Error Responses class API.

    A class that groups static error response functions.
    """

    @staticmethod
    def get_response( code, description, mime_type, title=None ):
        """Returns an HTTP flask response

        Parameters:
        ----------
        code:  int (required)
            The HTTP status code between 400 and 500 (inclusive)
        description: string (required)
            The text description related to the status
        mime_type: string (optional)
            The text corresponding to the mime-type
        title: string (optional)
            The text of a title to be rendered at an HTML page

        Returns:
        -------
        A Flask HTTP Response object

        Raises:
        ------
        Raises TypeError or ValueError if argument is not valid.
        """

        if not code or not isinstance( code, ( int ) ):
            raise TypeError( "code [{0}] is not valid".format( code ) )
        elif ( code < 400 ) or ( code > 500 ):
            raise ValueError( "code [{0}] is not valid. "
                             "It must be between 400 and 500"
                             .format( code ) )
        elif is_blank( description ):
            logging.warn( "error description is blank" )
            description = "no error description found"

        if re.search( "html", mime_type, flags=re.IGNORECASE ):
            body = ErrorResponse.get_html_response_body( 
                code,
                description,
                "HTTP Status Code:{0}".format( code ) )
            response = Response( body, status=code, mimetype="text/html" )
        elif re.search( "xml", mime_type, flags=re.IGNORECASE ):
            body = ErrorResponse.get_xml_response_body( code, description )
            response = Response( body, status=code, mimetype="application/xml" )
        elif re.search( "csv", mime_type, flags=re.IGNORECASE ):
            body = ErrorResponse.get_csv_response_body( code, description )
            response = Response( body, status=code, mimetype="text/csv" )
        elif re.search( "json", mime_type, flags=re.IGNORECASE ):
            response = ErrorResponse.get_json_response( code, description )
        else:  # default to JSON
            response = ErrorResponse.get_json_response( code, description )

        return response

    @staticmethod
    def get_html_response_body( code, description, title ):
        response = """
<!doctype html>

<html lang="en">
<head>
  <meta charset="utf-8">
  <title>HTTP Status Code -- [%d]</title>
</head>

<body>
<h1>%s</h1>
description = %s
</body>
</html>""" % ( code, title, cgi.escape( description ) )
        return response

    @staticmethod
    def get_xml_response_body( code, description ):
        response = """
<?xml version="1.0"?>
<error>
    <code>%d</code>
    <message>%s</message>
</error>""" % ( code, saxutils.escape( description ) )
        return response

    @staticmethod
    def get_csv_response_body( code, description ):
        output = io.StringIO()
        csv_data = [code, description]
        writer = csv.writer( output, quoting=csv.QUOTE_NONNUMERIC )
        writer.writerow( csv_data )
        row = output.getvalue()
        response = "code, message \r\n" + row
        return response

    @staticmethod
    def get_json_response( code, description ):
        error = OrderedDict()
        error["code"] = code
        error["message"] = description

        response = OrderedDict()
        response[STATUS_KEY] = STATUS_ERROR
        response["error"] = error

        ordered_response = jsonify( response )
        ordered_response.status_code = code

        return ordered_response

if __name__ == '__main__':
    pass
