from abc import ABCMeta

from twisted.python import log

from pi_time import config
from pi_time.models import api


class ApiBase:
    """
    Abstract base class for all API related classes.

    API classes are separated into logical groups, with all requests and
    responses sent using JSON data format.
    """

    __metaclass__ = ABCMeta

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = config.check_config_file(config_file)
        log.msg("%s is ready" % (self.__class__.__name__))

    def processRequest(self, request):
        if type(request) is not ApiRequest:
            raise TypeError('Expected ApiRequest in request ({} encountered)'.format(type(request)))
        log.msg('Processing API request %s' % (request.method))

    def processResponse(self, response):
        if type(response) is not ApiResponse:
            raise TypeError('Expected ApiResponse in request ({} encountered)'.format(type(response)))
        log.msg('Processing API response %s' % (request.method))
