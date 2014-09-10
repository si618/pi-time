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

    def get_sensors_config(self):
        return self.api.config['sensors']

    def get_sensor_config(self, sensor_name):
        name_config = json.loads(sensor_name)
        if 'name' not in name_config:
            raise Exception('Sensor name required')
        name = name_config['name']
        for sensor in self.api.config['sensors']:
            if sensor['name'] == name:
                return sensor
        raise Exception("Sensor '%s' not found in configuration" % name)

    def update_laptimer_config(self, laptimer_config):
        laptimer = json.loads(laptimer_config)
        config = update.update_laptimer(self.api.config_file, self.api.config,
            laptimer_config)
        return config

    def add_sensor(self, sensor_config):
        sensor = json.loads(sensor_config)
        config = update.add_sensor(self.api.config_file, self.api.config, 
            sensor)
        return config

    def update_sensor(self, sensor_config):
        sensor = json.loads(sensor_config)
        config = update.update_sensor(self.api.config_file, self.api.config,
            sensor)
        return config

    def rename_sensor(self, rename_config):
        sensor = json.loads(rename_config)
        if 'name' not in sensor:
            raise Exception('Sensor name required')
        if 'newName' not in sensor:
            raise Exception('Sensor newName required')
        sensor_name = sensor['name']
        new_sensor_name = sensor['newName']
        config = update.rename_sensor(self.api.config_file, self.api.config,
            sensor_name, new_sensor_name)
        return config

    def remove_sensor(self, name_config):
        sensor = json.loads(rename_config)
        if 'name' not in sensor:
            raise Exception('Sensor name required')
        sensor_name = sensor['name']
        config = update.remove_sensor(self.api.config_file, self.api.config,
            sensor_name)
        return config
