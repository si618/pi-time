from twisted.python import log


class ApiConfig:
    """API configuration methods."""

    def __init__(self, api):
        self.api = api

    def get_laptimer_config(self):
        return self.api.config['laptimer']

    def set_laptimer_config(self, laptimer_config):
        return

    def get_sensor_config(self, sensor_name):
        return

    def set_sensor_config(self, sensor_config):
        return
