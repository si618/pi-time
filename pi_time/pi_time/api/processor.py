import functools
import logging

import pi_time

from twisted.internet.defer import Deferred
from twisted.python import log

from pi_time import settings
from pi_time.api import config
from pi_time.config import check, options, update
from pi_time.models.api import ApiRequest, ApiResponse


# Tuple of associated class module for api method and event triggered
API_METHODS = (
    ('ApiConfig', 'add_sensor', None),
    ('ApiConfig', 'get_laptimer_config', None),
    ('ApiConfig', 'get_laptimer_options', None),
    ('ApiConfig', 'get_sensor_config', None),
    ('ApiConfig', 'get_sensor_options', None),
    ('ApiConfig', 'update_laptimer', 'laptimer_changed'),
    ('ApiConfig', 'update_sensor', 'sensor_changed'),
    ('ApiConfig', 'remove_sensor', 'sensor_changed'),
    ('ApiConfig', 'rename_sensor', 'sensor_changed'),
)

URI_PREFIX = 'io.github.si618.pi-time.'


class ApiProcessor(object):
    """Processes API requests, responses and event broadcasts."""

    def __init__(self, config_file, app_session=None):

        self._prefix = URI_PREFIX
        self.config = check.check_config_file(config_file)
        self.config_file = config_file
        self.api_config = config.ApiConfig(self)
        self.session = app_session

        log.msg("Pi-time API v{} ready".format(pi_time.API_VERSION))

    def register(self, method, params=None):
        """
        Register an api call and use convention-based approach to invoke method
        request as well as return an json encoded response."""

        reg = lambda: self.call(method, params).encode()
        name = self._prefix + method
        return self.session.register(reg, name)

    def call(self, method, params=None):
        """Invoke an api request and call for method in context."""
        if self.session is None:
            context = None
        else:
            context = self.session.context
        request = ApiRequest(method, context, params)
        response = self.process(request)
        return response

    def process(self, request):
        """Invoke an api request."""

        response = None
        try:
            response = self._processRequest(request)
            result = 'ok'
            if response.error is not None:
                result = response.error
            log.msg('Response {0} from {1} ({2})'.format(
                response.method, response.context, result,
                logLevel=logging.DEBUG))
            self._publishResponse(response)
        except Exception as exception:
            error = str(exception)
            log.err('API exception {}'.format(error))
            method = None
            context = None
            if type(response) is ApiResponse:
                method = response.method
                context = response.context
            response = ApiResponse(method, context, error=error)
        return response

    def _processRequest(self, request):
        """Processes an api request, including validation and publishing."""

        if type(request) is not ApiRequest:
            error = 'Request must be of type ApiRequest'
            return ApiResponse(method=None, context=None, error=error)

        msg = 'Request {} from {}'.format(request.method, request.context,
            logLevel=logging.DEBUG)
        if request.params is not None:
            msg += '({})'.format(request.params)
        log.msg(msg)

        api_match = [item for item in API_METHODS
            if item[1] == request.method]
        if len(api_match) == 0:
            error = "Unknown API method '{}'".format(request.method)
            return ApiResponse(request.method, request.context,
                error=error)

        method_class = self._get_method_class(api_match[0][0])
        method = getattr(method_class, request.method)

        # TODO: Go async using twisted deferred
        if request.params is None:
            data = method()
        else:
            data = method(request.params)
        return ApiResponse(request.method, request.context, data=data)

    def _get_method_class(self, method_class):
        """Gets the class associated with the method name."""

        if method_class == 'ApiConfig':
            return self.api_config

        raise ValueError("Unknown method class '{}'".format(method_class))

    def _publishResponse(self, response):
        """Publish response if associated with an api event."""

        if self.session is None:
            # Nothing to do
            return
        if response.error is not None:
             # Don't broadcast errors
            return
        api_match = [item for item in API_METHODS
            if item[1] == response.method and item[2] is not None]
        if len(api_match) == 0:
            # Nothing to do as no events for method
            return
        event_name = item[2]
        event = self._prefix + event_name
        log.msg('Publish {}'.format(event_name), logLevel=logging.DEBUG)
        self.session.publish(event)
