from autobahn import wamp

from pi_time.api import api
from pi_time.config import options, update


class ApiConfig(object):
    """API configuration methods."""

    def __init__(self, api):
        self.api = api

    #@api.method
    def get_laptimer_options(self):
        return options.get_laptimer_options()

    #@api.method
    def get_sensor_options(self):
        return options.get_sensor_options()

    #@api.method
    def get_laptimer_config(self):
        return self.api.config['laptimer']

    #@api.method
    def get_sensor_config(self):
        return self.api.config['sensors']

    #@api.method
    def update_laptimer(self, laptimer):
        return update.update_laptimer(self.api.config_file, self.api.config,
            laptimer)

    #@api.method(publish='sensor_changed')
    def add_sensor(self, sensor):
        return update.add_sensor(self.api.config_file, self.api.config,
            sensor)

    #@api.method(publish='sensor_changed')
    def update_sensor(self, sensor):
        return update.update_sensor(self.api.config_file, self.api.config,
            sensor)

    #@api.method(publish='sensor_changed')
    def rename_sensor(self, rename):
        if 'name' not in sensor:
            raise Exception('Sensor name required')
        if 'newName' not in sensor:
            raise Exception('Sensor newName required')
        return update.rename_sensor(self.api.config_file, self.api.config,
            sensor['name'], sensor['newName'])

    #@api.method(publish='sensor_changed')
    def remove_sensor(self, sensor):
        if 'name' not in sensor:
            raise Exception('Sensor name required')
        return update.remove_sensor(self.api.config_file, self.api.config,
            sensor['name'])
