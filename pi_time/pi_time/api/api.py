import logging

import pi_time

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


class Api(object):
    """Class responsible for API requests, responses and event broadcasts."""

    def __init__(self, config_file, app_session=None):

        self.config = check.check_config_file(config_file)
        self.config_file = config_file
        self.api_config = config.ApiConfig(self)
        self.session = app_session

        log.msg("Pi-time API v{} ready".format(pi_time.API_VERSION))

    def register(self, method, context, params=None):
        """
        Register an api call and use convention-based approach to invoke method
        request as well as return an json encoded response."""

        reg = lambda: self.call(method, context, params).encode()
        name = 'io.github.si618.pi-time.{}'.format(method)
        return self.session.register(reg, name)

    def call(self, method, context, params=None):
        """Invoke an api request and call for method in context."""

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
            log.msg("Response {} from {} ({})".format(
                response.method, response.context, result,
                logLevel=logging.DEBUG))
            self._publishResponse(response)
        except Exception as exception:
            log.err("API exception {}".format(exception))
            method = None
            context = None
            if type(response) is ApiResponse:
                method = response.method
                context = response.context
            response = ApiResponse(method, context, error=str(exception))
        return response

    def _processRequest(self, request):
        """Processes an api request, including validation and publishing."""

        if type(request) is not ApiRequest:
            error = "Expected ApiRequest but got {}".format(
                type(request).__name__)
            return ApiResponse(method=None, context=None,
                error=error)

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
        event = 'io.github.si618.pi-time.{}'.format(event_name)
        log.msg('Publish {}'.format(event_name), logLevel=logging.DEBUG)
        self.session.publish(event)
