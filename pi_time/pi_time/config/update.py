"""Module for updating configuration file."""
import json

from twisted.python import log

from pi_time.config import check


def update_laptimer(config_file, config, laptimer):
    """
    Updates the laptimer section of specified config_file after checking to
    ensure configuration is valid.

    :param config_file: Name of configuration file to update.
    :type config_file: str
    :param config: Complete current configuration.
    :type config: dict
    :param laptimer: Laptimer configuration to be updated.
    :type config_file: dict
    :returns: Complete configuration contents after being updated.
    :rtype: dict   
    """
    # Merges existing content, preferring new laptimer config for duplicates
    # TODO: Handle case when items are removed rather than updated or added.
    config['laptimer'].update(laptimer)
    check.check_laptimer(config['laptimer'])
    _update_config(config_file, config)
    log.msg('Updated laptimer configuration')
    return config


def add_sensor(config_file, config, sensor):
    """
    Adds the sensor section of specified config_file after checking to
    ensure sensor exists that the configuration is valid.

    :param config_file: Name of configuration file to update.
    :type config_file: str
    :param config: Complete current configuration.
    :type config: dict
    :returns: Complete configuration contents after being updated.
    :rtype: dict   
    """
    if 'name' not in sensor:
        raise Exception('Missing sensor name')
    name = sensor['name']
    match = None
    for s in config['sensors']:
        if s['name'] == name:
            match = s
            break
    if match is not None:
        raise Exception("Sensor '%s' already found in configuration" % name)
    check.check_sensor(sensor)
    # Merges existing content, preferring new sensor config for duplicates
    config['sensors'].append(sensor)
    _update_config(config_file, config)
    log.msg("Configuration added for sensor '%s'" % name)
    return config


def update_sensor(config_file, config, sensor):
    """
    Updates the sensor section of specified config_file after checking to
    ensure sensor exists that the configuration is valid.

    :param config_file: Name of configuration file to update.
    :type config_file: str
    :param config: Complete current configuration.
    :type config: dict
    :returns: Complete configuration contents after being updated.
    :rtype: dict   
    """
    if 'name' not in sensor:
        raise Exception('Missing sensor name')
    name = sensor['name']
    match = None
    index = 0
    for s in config['sensors']:
        if s['name'] == name:
            match = s
            break
        index += 1
    if match is None:
        raise Exception("Sensor '%s' not found in configuration" % name)
    # Merges existing content, preferring new sensor config for duplicates
    # TODO: Handle case when items are removed rather than updated or added.
    config['sensors'][index].update(sensor)
    check.check_sensor(config['sensors'][index])
    _update_config(config_file, config)
    log.msg("Configuration updated for sensor '%s'" % name)
    return config


def rename_sensor(config_file, config, sensor_name, new_sensor_name):
    """
    Renames sensor after checking the sensor exists in configuration and that
    the new sensor name is unique.

    :param config_file: Name of configuration file to update.
    :type config_file: str
    :param config: Complete current configuration.
    :type config: dict
    :param sensor_name: Existing sensor name.
    :type config_file: str
    :param sensor_name: Unique new sensor name.
    :type config_file: str
    :returns: Complete configuration contents after being updated.
    :rtype: dict   
    """
    if sensor_name is not None and sensor_name == new_sensor_name:
        return config
    match = None
    for sensor in config['sensors']:
        if sensor['name'] == sensor_name:
            match = sensor
        if sensor['name'] == new_sensor_name:
            raise Exception("Can't rename sensor '%s' as '%s' already "
                            "found in configuration" % (sensor_name, new_sensor_name))
    if match is None:
        raise Exception("Can't rename as existing sensor '%s' not found "
                        "in configuration" % sensor_name)
    match['name'] = new_sensor_name
    _update_config(config_file, config)
    log.msg("Configuration renamed from sensor '%s' to '%s'" % (sensor_name,
                                                                new_sensor_name))
    return config


def remove_sensor(config_file, config, sensor_name):
    """
    Removes sensor from configuration.

    :param config_file: Name of configuration file to update.
    :type config_file: str
    :param config: Complete current configuration.
    :type config: dict
    :param sensor_name: Name of sensor to remove.
    :type config_file: str
    :returns: Complete configuration contents after being updated.
    :rtype: dict   
    """
    match = None
    index = 0
    for sensor in config['sensors']:
        if sensor['name'] == sensor_name:
            match = sensor_name
        index += 1
    if match is None:
        raise Exception("Can't remove as sensor '%s' not found "
                        "in configuration" % sensor_name)
    del config['sensors'][index]
    _update_config(config_file, config)
    log.msg("Configuration for sensor '%s' removed" % sensor_name)
    return config


def _update_config(config_file, config):
    with open(config_file, 'w') as cfg:
        cfg.write(json.dumps(config, indent=4))
