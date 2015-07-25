"""rgapps.domain.sms module

This module contains SMS functionality.
"""
import logging

from rgapps.utils.exception import IllegalArgumentException
from rgapps.utils.utility import is_number, is_blank


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["SMS"]


class SMS:
    """ A Utility class used to send an SMS Text message to a celular phone.
    """

    MAX_MSG_LENGTH = 40
    MAX_PHONE_LENGTH = 20

    def send_text( self, phone_number, message ):
        """Sends given SMS message using http://textbelt.com/

        Parameters
        ----------
        phone_number:  str (required)
            recipient numeric string for a valid phone number. It cannot be
            greater than 20 digits
        message: str (optional)
            message to send. It cannot be greater than 40 characters.

        Returns
        -------
            nothing.
        """

        if is_blank( phone_number ):
            raise IllegalArgumentException( "phone_number is required" )

        if not is_number( phone_number ):
            raise IllegalArgumentException( 
                "phone_number [{0}] needs to be a number.".format( phone_number ) )

        if len( phone_number.strip() ) > self.MAX_PHONE_LENGTH:
            raise IllegalArgumentException( 
                 "phone_number [{0}] cannot be greater than [{1}]."
                .format( phone_number, self.MAX_PHONE_LENGTH ) )

        if is_blank( message ) :
            raise IllegalArgumentException ( "message cannot blank" )


        if len( message.strip() ) > self.MAX_MSG_LENGTH:
            raise IllegalArgumentException( 
                "message [{0}] cannot be greater than [{1}]."
                .format( message, self.MAX_MSG_LENGTH ) )

        url = 'http://textbelt.com/text'
        payload = {'number': phone_number,
                   'message': "iotgw.rubens.home: " + message.strip()}

        logging.debug( "Sending SMS to [{0}] using url [{1}]"
                      .format( phone_number, url ) )

        import requests
        r = requests.post( url, data=payload )

        if ( r.status_code != 200 ):
            logging.debug( "Failed SMS to [{0}] using url [{1}]: error coe [{2}]"
                          .format( phone_number, url, r.status_code ) )
            r.raise_for_status()

        return



if __name__ == '__main__':
    pass
