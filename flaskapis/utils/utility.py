"""flaskapis.utils.utility module

This module contains common utility functions.
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["get_log_file_handles", "is_number",
           "decimal_places", "write_to_file", "EMail", "SMS"]


from decimal import Decimal
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from flask import current_app
from validate_email import validate_email
from werkzeug.exceptions import BadRequest


class EMail:
    """A EMail class to send emails
    """

    def send_email(self, recipient, subject, message):
        """Sends given message using Gmail credentials defined in the
        application.cfg file.

        Parameters
        ----------
        recipient:  str (required)
            recipient email address
        subject:  str (optional)
            email subject
        message: str (optional)
            message to send

        Returns
        -------
            nothing.

        Raises
        ------
        SMTPHeloError:
            The server didn't reply properly to the helo greeting.
        SMTPAuthenticationError:
            The server didn't accept the username/password combination.
        SMTPException:
            No suitable authentication method was found.
        SMTPRecipientsRefused:
          The server rejected ALL recipients (no mail was sent).
        SMTPSenderRefused:
            The server didn't accept the from_addr.
        SMTPDataError:
            The server replied with an unexpected error code (other than a
            refusal of a recipient).
        """

        if "GMAIL_ACCOUNT" not in current_app.config:
            raise EnvironmentError("GMAIL_ACCOUNT property missing "
                                   "in application.cfg")

        # ensure valid GMail Account
        is_valid = validate_email(current_app.config['GMAIL_ACCOUNT'].strip())

        if(not is_valid):
            raise EnvironmentError(
                                "GMail Account [{0}] is not valid email address"
                               .format(current_app.config['GMAIL_ACCOUNT']))

        if "GMAIL_PASSWORD" not in current_app.config:
            raise EnvironmentError("GMAIL_PASSWORD property missing "
                                   "in application.cfg")

        gmail_user = current_app.config['GMAIL_ACCOUNT'].strip()
        gmail_password = current_app.config['GMAIL_PASSWORD'].strip()

        current_app.logger.debug(
           "Sending email using Gmail account [{0}] to recipient [{1}]"
           .format(gmail_user, recipient)
        )

        is_valid = validate_email(recipient)

        if(not is_valid):
            raise BadRequest("Recipient [{0}] is not valid email address"
                             .format(recipient))

        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        current_app.logger.debug("Sending email to [{0}] usgin Gmail "
                                 "account [{1}]"
                                 .format(recipient, gmail_user))

        mail_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        mail_server.login(gmail_user, gmail_password)
        failed_recipients = mail_server.sendmail(
            gmail_user, recipient, msg.as_string()
        )
        if failed_recipients:
            current_app.logger.warn(
                "Email failed to following recipients [{0}]"
                .format(failed_recipients)
                )
        mail_server.close()

        return


class SMS:
    """ A Utility class used to send an SMS Text message to a celular phone.
    """

    MAX_MSG_LENGTH = 40
    MAX_PHONE_LENGTH = 20

    def send_text(self, phone_number, message):
        """Sends given SMS message using http://textbelt.com/

        Parameters
        ----------
        phone_number:  str (required)
            recipient valid phone number. It cannot be greater than 20 digits
        message: str (optional)
            message to send. It cannot be greater than 40 characters.

        Returns
        -------
            nothing.

        Raises
        ------
        BadRequest if an argument is invalid.
        """
        if (not phone_number or len(phone_number.strip()) == 0 or
            not is_number(phone_number)):
            raise BadRequest ("phone_number [{0}] needs to be a number."
                              .format(phone_number))

        if len(phone_number.strip()) > self.MAX_PHONE_LENGTH:
            raise BadRequest ("phone_number [{0}] cannot be greater than [{1}]."
                              .format(phone_number, self.MAX_PHONE_LENGTH))

        if not message or len(message.strip()) == 0 :
            raise BadRequest("message cannot blank")


        if len(message.strip()) > self.MAX_MSG_LENGTH:
            raise BadRequest ("message [{0}] cannot be greater than [{1}]."
                                .format(message, self.MAX_MSG_LENGTH))

        url = 'http://textbelt.com/text'
        payload = {'number': phone_number,
                   'message': "iotgw.rubens.home: " + message.strip()}

        current_app.logger.debug("Sending SMS to [{0}] using url [{1}]"
                                 .format(phone_number, url))

        import requests
        r = requests.post(url, data=payload)

        if (r.status_code != 200):
            current_app.logger.debug("Failed SMS to [{0}] using url [{1}]: "
                                     "error coe [{2}]"
                                     .format(phone_number, url, r.status_code))
            r.raise_for_status()

        return


def is_number(arg):
    """
    Checks if arg is a number.

    Parameters
    ----------
    arg: string
        An argument that wants to check to see if it is a number.
        A number can be float, int or complex.

    Returns
    -------
    True: if it is a number
    False: if it is not a number
    """
    if not arg:
        return False

    try:
        float(arg)  # for int, long and float

    except ValueError:
        try:
            complex(arg)  # for complex
        except ValueError:
            return False

    return True


def decimal_places(arg):
    """
    Returns the number of decimal places in the given number
    Parameters
    ----------
    arg: Numeric or string
        A number to determine the number of decimal places

    Returns
    -------
    Number of decimal places found.

    Raises
    ------
    TypeError if argument is not numeric.
    """
    if not is_number(str(arg)):
        raise TypeError(("[{0}] is not a number").format(arg))

    dec = Decimal(str(arg))
    exp = dec.as_tuple().exponent
    result = -exp

    return result


def write_to_file(msg, fileToWrite):
    """ Simple utility to write to file.

    It is to replace the following that has been deprecated in Python 3.4:
        print >> file, "some text

    Parameters
    ----------
    msg: string (optional)
        A text message
    fileToWrite: file (required)
        An existing writeable file

    Returns
    -------
    Nothing
    """

    if fileToWrite and not fileToWrite.closed:
        fileToWrite.write(msg)

    return


def get_log_file_handles(logger):
    """ Returns a list of the file descriptors used by the given
    logging.logger.  This method may be used by the DaemonContext
    files_preserve when creating daemon on Linux environment.

    Parameters
    ----------
    logger: logging.logger (ooptional)

    Returns
    -------
    List containing all the file handle descriptors used by the given logger.
    """
    handles = []

    if logger:

        for handler in logger.handlers:
            handles.append(handler.stream.fileno())

        if logger.parent:
            handles += get_log_file_handles(logger.parent)

    return handles



if __name__ == '__main__':
    pass
