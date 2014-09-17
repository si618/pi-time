import functools
import logging

import wrapt

import pi_time

from twisted.python import log

from pi_time import settings
from pi_time.config import check, options, update


def api_method(wrapped=None, publish=None):
    """
    Decorator for API methods.

    Logs details and publishes decorated event after method executes.
    """

    if wrapped is None:
        return functools.partial(api_method, publish=publish)

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        msg = 'Call {}'.format(wrapped.__name__)
        if len(args) > 0:
            msg += ', args {}'.format(args)
        if len(kwargs) > 0:
            msg += ', kwargs {}'.format(kwargs)
        log.msg(msg, logLevel=logging.DEBUG)
        data = wrapped(*args, **kwargs)
        if publish and instance.session:
            log.msg('Publish {}'.format(publish), logLevel=logging.DEBUG)
            instance.session.publish(settings.URI_PREFIX + publish)
        return data
    return wrapper(wrapped)


class Api(object):

    def __init__(self, session, config_file):
        self.session = session
        self.config = check.check_config_file(config_file)
        self.config_file = config_file

        log.msg('Pi-time API v{} ready'.format(pi_time.API_VERSION))

    @api_method
    def get_laptimer_options(self):
        return options.get_laptimer_options()

    @api_method
    def get_laptimer_config(self):
        return self.config['laptimer']

    @api_method
    def get_sensor_options(self):
        return options.get_sensor_options()

    @api_method
    def get_sensor_config(self):
        return self.config['sensors']

    @api_method(publish='laptimer_changed')
    def update_laptimer(self, laptimer):
        return update.update_laptimer(self.config_file, self.config,
            laptimer)

    @api_method(publish='sensor_changed')
    def add_sensor(self, sensor):
        return update.add_sensor(self.config_file, self.config,
            sensor)

    @api_method(publish='sensor_changed')
    def update_sensor(self, sensor):
        return update.update_sensor(self.config_file, self.config,
            sensor)

    @api_method(publish='sensor_changed')
    def rename_sensor(self, sensor_name, new_sensor_name):
        return update.rename_sensor(self.config_file, self.config,
            name, new_name)

    @api_method(publish='sensor_changed')
    def remove_sensor(self, sensor_name):
        return update.remove_sensor(self.config_file, self.config,
            sensor_name)
