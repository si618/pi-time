import jsonpickle

import pi_time

from abc import ABCMeta

class ApiFormatBase:
    """
    Abstract base classes for all API calls.

    Follows style guide:
    https://google-styleguide.googlecode.com/svn/trunk/jsoncstyleguide.xml
    """

    __metaclass__ = ABCMeta

    def __init__(self, method, context):
        """
        Initialises common attributes apiVersion, method and context.

        All derived classes should call this via super.

        :param method: API method to invoke.
        :type method: str
        :param context: Context of client making API call.
        :type context: str
        """
        self.apiVersion = pi_time.API_VERSION
        self.method = method
        self.context = context

    def toJSON(self):
        """Converts object to Javascript Object Notation."""
        clone = copy.deepcopy(self)
        return jsonpickle.encode(clone, unpicklable=False)


class ApiRequest(ApiFormatBase):
    """Request data format for API calls."""

    def __init__(self, method, context, params=None):
        """
        :param method: API method to invoke.
        :type method: str
        :param context: Context of client making API call.
        :type context: str
        :param params: Optional request parameters.
        :type params: object
        """
        super(ApiRequest, self).__init__(method, context)
        self.params = params


class ApiResponse(ApiFormatBase):
    """Response data format for results from API calls."""

    def __init__(self, method, context, data=None, error=None):
        """
        :param method: API method to invoke.
        :type method: str
        :param context: Context of client making API call.
        :type context: str
        :param data: Contains any payload data.
        :type data: object
        :param error: Details any errors.
        :type error: object
        """
        super(ApiResponse, self).__init__(method, context)
        self.data = data
        self.error = error
