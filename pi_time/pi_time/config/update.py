import json

from twisted.python import log

from pi_time import settings
from pi_time.config import check


def update_laptimer(config_file, config, laptimer):
    """
    Updates the laptimer section of specified config_file after checking to
    ensure configuration is valid.

    :param config_file: Name of configuration file. Assumed to exist.
    :type config_file: str
    :param config: Complete current configuration. Assumed already checked.
    :type config: dict
    :param laptimer: Laptimer configuration to be updated.
    :type config_file: dict
    :returns: Complete configuration contents in dictionary format.
    :rtype: dict   
    """
    if 'laptimer' not in laptimer:
        raise Exception('Unable to find laptimer in config')
    # Merges existing content, prefering new laptimer config for duplicates
    config['laptimer'] += check.check_laptimer(laptimer)
    _update_config(config_file, config)
    log.msg('Updated laptimer configuration')


def update_sensor(config_file, config, sensor):
    """
    Updates the sensor section of specified config_file after checking to
    ensure configuration is valid.

    The sensor.name property must be present and is used to either update an
    existing sensor section based on name match, or adds a new one if no match
    is found.

    :param config_file: Name of configuration file. Assumed to exist.
    :type config_file: str
    :param config: Complete current configuration. Assumed already checked.
    :type config: dict
    :param laptimer: Sensor configuration to be updated.
    :type config_file: dict
    :returns: Complete configuration contents in dictionary format.
    :rtype: dict   
    """
    sensor = check.check_sensor(sensor)
    match = None
    for s in config['sensors']:
        if s.name == sensor.name:
            match = s
            break
    if match is None:
        config['sensors'].insert(sensor)
    else:
        # Merges existing content, prefering new sensor config for duplicates
        config['sensors'][sensor.name] += sensor 
    _update_config(config_file, config)
    log.msg('Updated sensor: %s configuration' % (sensor.name))
     

def _update_config(config_file, config):
    with open(config_file, 'w') as cfg:
        cfg.write(config)
