import copy
import jsonpickle

import pi_time

from abc import ABCMeta

from pi_time import settings

class ApiDataFormat(object):
    """
    Abstract base class to define data format for rpc, pubsub and event 
    handling triggered via API.

    Follows style guide:
    https://google-styleguide.googlecode.com/svn/trunk/jsoncstyleguide.xml
    """

    __metaclass__ = ABCMeta

    def __init__(self, method, context):
        """
        Initialises common attributes apiVersion, method and context.

        Validates method is valid API call.

        All derived classes should call this via super.

        :param method: API method to invoke.
        :type method: str
        :param context: Context of client.
        :type context: str
        """

        self.apiVersion = pi_time.API_VERSION
        self.method = method
        self.context = context

    def encode(self):
        """Converts object to Javascript Object Notation."""
        clone = copy.deepcopy(self)
        return jsonpickle.encode(clone, unpicklable=False)


class ApiRequest(ApiDataFormat):
    """Request data format for API calls."""

    def __init__(self, json_data):
        """
        Initialises attributes from json data and validates parameters.

        :param method: API method to invoke.
        :type method: str
        :param context: Context of client.
        :type context: str
        :param params: Optional request parameters.
        :type params: object
        """
        data = json.loads(json_data)

        super(ApiRequest, self).__init__(method, context)
        self.params = params


    def __init__(self, method, context, params=None):
        """
        Initialises attributes and validates parameters against method.

        :param method: API method to invoke.
        :type method: str
        :param context: Context of client.
        :type context: str
        :param params: Optional request parameters.
        :type params: object
        """
        super(ApiRequest, self).__init__(method, context)
        self.params = params


class ApiResponse(ApiDataFormat):
    """Response data format for results of API calls."""

    def __init__(self, method, context, data=None, error=None):
        """
        :param method: API method to invoke.
        :type method: str
        :param context: Context of client.
        :type context: str
        :param data: Contains any payload data.
        :type data: object
        :param error: Details of any errors.
        :type error: object
        """
        super(ApiResponse, self).__init__(method, context)
        self.data = data
        self.error = error


class ApiEvent(ApiResponse):
    """Data format for events triggered ."""

    def __init__(self, event, context, data=None):
        """
        :param event: API event invoked.
        :type event: str
        :param context: Context of client.
        :type context: str
        :param data: Contains any payload data.
        :type data: object
        :param error: Details of any errors.
        :type error: object
        """
        super(ApiEvent, self).__init__(method, context)
        self.data = data
        self.error = error
