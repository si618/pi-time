from twisted.python import log

from pi_time import configcheck
from pi_time.api import config
from pi_time.models.rpc import RpcRequest, RpcResponse


class Api:
    """
    Class responsible for handling API related requests and responses.

    API methods are separated into logical modules, with all requests and
    responses sent using JSON data format.
    """

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configcheck.check_config_file(config_file)
        log.msg("API ready")

    def process(self, request):
        try:
            response = self._processRequest(request)
        except Exception as e:
            # _processRequest checks for RpcRequest type
            method = request.method
            context = request.context
            log.err('Exception caught in %s: %s' % (method, e))
            # TODO: Helper method to build exception based rpc error
            error = type(e).__name__
            response = RpcResponse(method, context, error=error)
        return response.toJSON()

    def _processRequest(self, request):
        if type(request) is not RpcRequest:
            error = 'Expected RpcRequest type ' \
                '({} encountered)'.format(type(request))
            response = RpcResponse(method, context, error=error)
            return response
        log.msg('Processing API request %s' % (request.method))
        response = RpcResponse(request.method, request.context)
        return response


