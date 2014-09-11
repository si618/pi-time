from twisted.python import log

from pi_time import settings
from pi_time.api import config
from pi_time.config import check, options, update
from pi_time.models.rpc import RpcRequest, RpcResponse


class Api(object):
    """
    Class responsible for handling API related requests and responses.

    API methods are separated into logical modules, with all requests and
    responses sent using JSON data format.
    """

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = check.check_config_file(config_file)
        self.api_methods = zip(*settings.API)[0]
        log.msg("Pi-time API is ready to roll")

    def process(self, request):
        try:
            response = self._processRequest(request)
        except Exception as e:
            log.err("Exception caught: %s" % e)
            if type(response) is RpcResponse:
                method = response.method
                context = response.context
                error = type(e).__name__
            else:
                method = '<unknown>'
                context = '<unknown>'
                error = str(e)
            response = RpcResponse(method, context, error=error)
        log.msg("Returning API response '%s'" % (response.method))
        return response.toJSON()

    def _processRequest(self, request):
        if type(request) is not RpcRequest:
            error = "Expected RpcRequest type " \
                "({} encountered)".format(type(request).__name__)
            response = RpcResponse('<unknown>', context='<unknown>',
                error=error)
            return response
        if request.method not in self.api_methods:
            error = "Unknown API method '{}'".format(request.method)
            response = RpcResponse(request.method, request.context,
                error=error)
            return response
        log.msg("Processing API request '%s'" % (request.method))
        api_class = settings.API[request.method][1]
        # https://xkcd.com/353/ ;-)
        method = getattr(api_class, request.method)
        data = method(**request.params)
        response = RpcResponse(request.method, request.context, data=data)
        return response