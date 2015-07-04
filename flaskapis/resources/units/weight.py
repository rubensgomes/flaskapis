"""flaskapis.resources.units.weight module

This module contains the REST API source code for weight conversion.
"""

__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["Weight"]

from flask import request, jsonify
from flask.ext.restful import Resource
from werkzeug.exceptions import BadRequest

from flaskapis.enums import UNIT_TYPES_ENUM
from flaskapis.resources.units import convert_unit
from flaskapis.utils.utility import is_number


class Weight(Resource):
    """REST API Resource to convert weights
    """

    def get(self, to_unit):
        """REST GET implementation for the URI:

        http://<server>:<port>/weight/<to_unit>?from_unit=<from_unit>&
            from_value=<from_value>

        Parameters
        ----------
        to_unit:  str (required)
            length unit (required)

        It is assumed that this method is called within the context of an HTTP
        request.  And that the HTTP request contains query parameters
        with the request.args as containing the following:

        from_unit: str (required)
            mass unit
        from_value: str (required)
            numeric value

        Returns
        -------
        str:
            A JSON string containing the response

        Raises
        ------
        BadRequest if there is an error validating the input parameters or
        some other error processing this method.
        """
        params = request.args
        if not params:
            raise BadRequest("Parameters "
                             "from_unit=<from_unit>&from_value=<_from_value> "
                             "are missing")

        if not isinstance(params, dict):
            raise BadRequest("params must be an instance of dict")

        if "from_unit" not in params:
            raise BadRequest("Missing required from_unit parameter")

        if "from_value" not in params:
            raise BadRequest("Missing required from_value parameter")

        from_unit = params.get("from_unit")

        from_value = params.get("from_value")
        if not is_number(from_value):
            raise BadRequest(("Parameter from_value=[{0}] not valid. "
                              "A numeric value must be provided.")
                             .format(from_value))

        if from_unit == to_unit:
            raise BadRequest("from_unit=[{0}] and to_unit=[{1}] units "
                             "cannot be equal".format(from_unit, to_unit))

        # pint unit registry only accepts lower case letters for mass units
        from_unit = from_unit.lower().strip()
        to_unit = to_unit.lower().strip()

        result = convert_unit(UNIT_TYPES_ENUM.mass,
                              from_unit, from_value, to_unit)
        return jsonify(result)


if __name__ == "__main__":
    pass
