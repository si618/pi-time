from twisted.python import log

from pi_time import checkconfig


class Api:
    """
    TODO: API methods...
    """

    def __init__(self, config_file):
        self.config = checkconfig.check_config_file(config_file)
        log.msg("Pi-time API initialised")
