import logging

import pi_time

from twisted.python import log

from pi_time import settings
from pi_time.api import config
from pi_time.config import check, options, update
from pi_time.models.api import ApiRequest, ApiResponse


class Api(object):
    """Class responsible for handling API related requests and responses."""

    def __init__(self, config_file, applicationSession=None):

        self.config = check.check_config_file(config_file)
        self.config_file = config_file
        self.api_config = config.ApiConfig(self)
        self.session = applicationSession

        log.msg("Pi-time API v{} ready".format(pi_time.API_VERSION))

    def call(self, method, context, params=None):

        request = ApiRequest(method, context, params)
        response = self.process(request)
        return response

    def process(self, request):

        response = None
        try:
            response = self._processRequest(request)
            result = 'ok'
            if response.error is not None:
                result = response.error
            log.msg("API response {} from {} ({})".format(
                response.method, response.context, result,
                logLevel=logging.DEBUG))
            self._processResponse(response)
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

        if type(request) is not ApiRequest:
            error = "Expected ApiRequest but got {}".format(
                type(request).__name__)
            return ApiResponse(method=None, context=None,
                error=error)

        msg = 'API request {} from {}'.format(request.method, request.context,
            logLevel=logging.DEBUG)
        if request.params is not None:
            msg += '({})'.format(request.params)
        log.msg(msg)

        api_match = [item for item in settings.API
            if item[1] == request.method]
        if len(api_match) == 0:
            error = "Unknown API method '{}'".format(request.method)
            return ApiResponse(request.method, request.context,
                error=error)

        method_class = self._get_method_class(api_match[0][0])
        method = getattr(method_class, request.method)

        if request.params is None:
            data = method()
        else:
            data = method(request.params)
        return ApiResponse(request.method, request.context, data=data)

    def _get_method_class(self, method_class):

        if method_class == 'ApiConfig':
            return self.api_config

        raise ValueError("Unknown method class '{}'".format(method_class))

    def _processResponse(self, response):

        if self.session is None:
            # Nothing to do
            return
        if response.error is not None:
             # Don't broadcast errors
            return
        api_match = [item for item in settings.API
            if item[1] == response.method and item[2] is not None]
        if len(api_match) == 0:
            # Nothing to do as no events for method
            return
        event_name = item[2]
        event = 'io.github.si618.pi-time.{}'.format(event_name)
        log.msg('API publish {}'.format(event_name), logLevel=logging.DEBUG)
        self.session.publish(event)
