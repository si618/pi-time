from twisted.python import log

from pi_time.config import options, update


class ApiConfig(object):
    """API configuration methods."""

    def __init__(self, api):
        self.api = api

    def get_laptimer_options(self):
        return options.get_laptimer_options()

    def get_sensor_options(self):
        return options.get_sensor_options()

    def get_laptimer_config(self):
        return self.api.config['laptimer']

    def get_sensor_config(self):
        return self.api.config['sensors']

    def update_laptimer(self, laptimer):
        config = update.update_laptimer(self.api.config_file, self.api.config,
            laptimer)
        return config

    def add_sensor(self, sensor):
        config = update.add_sensor(self.api.config_file, self.api.config,
            sensor)
        return config

    def update_sensor(self, sensor):
        config = update.update_sensor(self.api.config_file, self.api.config,
            sensor)
        return config

    def rename_sensor(self, rename):
        if 'name' not in sensor:
            raise Exception('Sensor name required')
        if 'newName' not in sensor:
            raise Exception('Sensor newName required')
        sensor_name = sensor['name']
        new_sensor_name = sensor['newName']
        config = update.rename_sensor(self.api.config_file, self.api.config,
            sensor_name, new_sensor_name)
        return config

    def remove_sensor(self, sensor):
        if 'name' not in sensor:
            raise Exception('Sensor name required')
        sensor_name = sensor['name']
        config = update.remove_sensor(self.api.config_file, self.api.config,
            sensor_name)
        return config
