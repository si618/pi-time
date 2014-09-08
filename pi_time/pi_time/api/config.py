from twisted.python import log

from pi_time import config
from pi_time.api import base


class ApiConfig(base.ApiBase):
    """API configuration methods..."""

    def get_laptimer_config(self):
        return self.config['laptimer']

    def set_laptimer_config(self, laptimer_config):
        return

    def get_sensor_config(self, sensor_name):
        return

    def set_sensor_config(self, sensor_config):
        return
