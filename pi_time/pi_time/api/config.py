from twisted.python import log

from pi_time.config import options, update


class _ApiConfig(object):
    """API configuration methods."""

    def __init__(self, api):
        self.api = api

    def get_laptimer_options(self):
        return options.get_laptimer_options()

    def get_sensor_options(self):
        return options.get_sensor_options()

    def get_laptimer_config(self):
        return self.api.config['laptimer']

    def get_sensor_config(self, sensor_name):
        sensors = self.api.config['sensors']
        for sensor in sensors:
            if sensor['name'] == sensor_name:
                return sensor
        raise Exception('TODO: Sensor not found')

    def set_laptimer_config(self, laptimer_config):
        update.update_laptimer(self.api.config_file, self.api.config, 
            laptimer_config)
        raise Exception('TODO: Not yet implemented')

    def set_sensor_config(self, sensor_config):
        update.update_sensor(self.api.config_file, self.api.config, 
            sensor_config)
        raise Exception('TODO: Not yet implemented')
