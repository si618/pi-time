# Configuration code shamelessly based on Crossbar.io checkconfig.py
import yaml

from autobahn.websocket.protocol import parseWsUrl
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
        if k not in ['name', 'url', 'unitOfMeaurement']:
            raise Exception("Encountered unknown attribute '{}' in laptimer configuration".format(k))

    #if 'unit' in laptimer

def check_sensor(sensor, silence=False):
    """
    Check a sensor configuration item.

    :param sensor: The sensor configuration to check.
    :type sensor: dict
    :param silence: Whether to log configuration checks. Defaults to false.
    :type silence: boolean
    """
    if type(sensor) != dict:
        raise Exception("sensor items must be dictionaries ({} encountered)\n\n{}".format(type(sensor),
            pformat(sensor)))

    for k in sensor:
        if k not in ['name', 'url', 'location', 'position', 'hardware',
        'pinActiveApp', 'pinActiveLap', 'pinEventTrigger']:
            raise Exception("Encountered unknown attribute '{}' in sensor configuration".format(k))

    #if 'url' in sensor:

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

def check_config_file(config_file, silence=False):
    """
    Check a pi-time configuration file.

    :param config_file: The file to check.
    :type config_file: str
    :param silence: Whether to log configuration checks. Defaults to false.
    :type silence: boolean
    """
    configext = os.path.splitext(config_file)[1]
    config_file = os.path.abspath(config_file)

    with open(config_file, 'rb') as infile:
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