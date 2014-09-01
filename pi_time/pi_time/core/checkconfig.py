# Configuration code shamelessly taken from Crossbar.io checkconfig.py

import yaml

from twisted.python import log
from yaml import Loader, SafeLoader

# Hack: force PyYAML to parse _all_ strings into Unicode
# http://stackoverflow.com/a/2967461/884770
def construct_yaml_str(self, node):
    return self.construct_scalar(node)

Loader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)
SafeLoader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)


def check_laptimer(laptimer, silence=False):
    """
    Check a laptimer configuration item.

    :param laptimer: The laptimer configuration to check.
    :type laptimer: dict
    :param silence: Whether to log configuration checks. Defaults to false.
    :type silence: boolean
    """
    for k in laptimer:
        if k not in ['name', 'address', 'unit']:
            raise Exception("encountered unknown attribute '{}' in laptimer configuration".format(k))

    #if 'unit' in laptimer



def check_sensor(sensor, silence=False):
    """
    Check a sensor configuration item.

    :param sensor: The sensor configuration to check.
    :type sensor: dict
    :param silence: Whether to log configuration checks. Defaults to false.
    :type silence: boolean
    """
    if type(controller) != dict:
        raise Exception("sensor items must be dictionaries ({} encountered)\n\n{}".format(type(controller), pformat(controller)))

    for k in sensor:
        if k not in ['name', 'address', 'type', 'position']:
            raise Exception("encountered unknown attribute '{}' in sensor configuration".format(k))

    #if 'address' in sensor:
    #    check_address(sensor['id'])


def check_config(config, silence=False):
    """
    Check a pi-time top-level configuration.

    :param config: The configuration to check.
    :type config: dict
    :param silence: Whether to log configuration checks. Defaults to false.
    :type silence: boolean
    """

    if type(config) != dict:
   	    raise Exception(
            "Top-level configuration item must be a dictionary ({} encountered)".format(type(config)))

    for k in config:
        if k not in ['laptimer', 'sensors']:
            raise Exception("Encountered unknown attribute '{}' in top-level configuration".format(k))

    # check laptimer config
    if 'laptimer' in config:
        if not silence:
            log.msg("Checking laptimer item ..")
                check_laptimer(config['laptimer'])

    # check sensors config
    sensors = config.get('sensors', [])

    if type(sensors) != list:
        raise Exception("'sensors' attribute in top-level configuration must be a list ({} encountered)".format(type(sensors)))

    i = 1
    for sensor in sensor:
        if not silence:
            log.msg("Checking sensor item {} ..".format(i))
            check_sensor(sensor, silence)
            i += 1


def check_config_file(configfile, silence=False):
    """
    Check a pi-time configuration file.

    :param configfile: The file to check.
    :type configfile: str
    :param silence: Whether to log configuration checks. Defaults to false.
    :type silence: boolean
    """
    configext = os.path.splitext(configfile)[1]
    configfile = os.path.abspath(configfile)

    with open(configfile, 'rb') as infile:
    if configext == '.yaml':
        try:
            config = yaml.safe_load(infile)
        except Exception as e:
            raise Exception("Configuration file does not seem to be proper YAML ('{}'')".format(e))
    else:
        try:
            config = json.load(infile)
        except ValueError as e:
            raise Exception("Configuration file does not seem to be proper JSON ('{}'')".format(e))

    check_config(config, silence)

    return config
