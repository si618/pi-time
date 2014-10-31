"""Module for API related code."""
import logging

import pi_time

from autobahn import wamp

from twisted.python import log

from pi_time import settings
from pi_time.config import check, options, update


class Api(object):
    """
    Defines the procedures available to be called from laptimer or sensor apps
    and their clients.

    If a procedure has an associated event, the event publishes the result and
    the procedure returns nothing. This avoids duplicating data sent over the
    wire, but assumes client calling the procedure is also subscribed to the
    event.
    """

    def __init__(self, session, config_file):
        self.session = session
        self.config = check.check_config_file(config_file)
        self.config_file = config_file

        log.msg("Pi-time API v{} ready".format(pi_time.API_VERSION))

    def _publish(self, event, data=None):
        if self.session:
            self.session.publish(settings.URI_PREFIX + event, data)
            log.msg("Published {}".format(event), logLevel=logging.DEBUG)

    @wamp.register(u"pi-time.get_laptimer_options")
    def get_laptimer_options(self):
        return options.get_laptimer_options()

    @wamp.register(u"pi-time.get_laptimer_config")
    def get_laptimer_config(self):
        return self.config["laptimer"]

    @wamp.register(u"pi-time.get_sensor_options")
    def get_sensor_options(self):
        return options.get_sensor_options()

    @wamp.register(u"pi-time.get_sensor_config")
    def get_sensor_config(self):
        return self.config["sensors"]

    @wamp.register(u"pi-time.update_laptimer")
    def update_laptimer(self, laptimer):
        config = update.update_laptimer(self.config_file, self.config,
                                        laptimer)
        if "laptimer" in config:
            self.config = config
            self._publish("laptimer_changed", config["laptimer"])

    @wamp.register(u"pi-time.add_sensor")
    def add_sensor(self, sensor):
        config = update.add_sensor(self.config_file, self.config,
                                   sensor)
        if "sensors" in config:
            self.config = config
            self._publish("sensor_changed", config["sensors"])

    @wamp.register(u"pi-time.update_sensor")
    def update_sensor(self, sensor):
        config = update.update_sensor(self.config_file, self.config,
                                      sensor)
        if "sensors" in config:
            self.config = config
            self._publish("sensor_changed", config["sensors"])

    @wamp.register(u"pi-time.rename_sensor")
    def rename_sensor(self, sensor_name, new_sensor_name):
        config = update.rename_sensor(self.config_file, self.config,
                                      sensor_name, new_sensor_name)
        if "sensors" in config:
            self.config = config
            self._publish("sensor_changed", config["sensors"])

    @wamp.register(u"pi-time.remove_sensor")
    def remove_sensor(self, sensor_name):
        config = update.remove_sensor(self.config_file, self.config,
                                      sensor_name)
        if "sensors" in config:
            self.config = config
            self._publish("sensor_changed", config["sensors"])
