# Code based on Crossbar.io checkconfig.py (with thanks!:)
import json
import logging
import os
import yaml

import pytz
import six

from pprint import pformat

from autobahn.websocket.protocol import parseWsUrl

from twisted.python import log

from pi_time import settings


def check_name(config, section):
    if 'name' in config:
        name = config['name']
        if type(name) != six.text_type:
            raise Exception("'name' in {} configuration must be str ({} " \
                "encountered)".format(section, type(name)))


def check_url(config, section):
    if 'url' in config:
        url = config['url']
        if type(url) != six.text_type:
            raise Exception("'url' in {} configuration must be str ({} " \
                "encountered)".format(section, type(url)))
        try:
            u = parseWsUrl(url)
        except Exception as e:
            raise Exception("Invalid 'url' in {} configuration : {}".format(
                section, e))
    else:
        raise Exception("'url' required in {} configuration".format(section))


def check_unit_of_measurement(laptimer):
    if 'unitOfMeasurement' in laptimer:
        unit = laptimer['unitOfMeasurement']
        units = zip(*settings.CHOOSE_UNIT_OF_MEASUREMENT)[0]
        if unit not in units:
            raise Exception("'unitOfMeasurement' in laptimer configuration " \
                "must be {} ({} encountered)".format(units, unit))


def check_timezone(laptimer):
    if 'timezone' in laptimer:
        timezone = laptimer['timezone']
        if timezone not in pytz.common_timezones:
            raise Exception("'timezone' in laptimer configuration must be " \
                "valid entry in pytz.common_timezones ({} encountered)".format(
                timezone))


def check_sensor_location(sensor):
    if 'location' in sensor:
        location = sensor['location']
        locations = zip(*settings.CHOOSE_SENSOR_LOCATION)[0]
        if location not in locations:
            raise Exception("'location' in sensor configuration must be {} " \
                "({} encountered)".format(locations, location))


def check_sensor_position(sensor):
    if 'position' in sensor:
        position = sensor['position']
        if type(position) not in six.integer_types:
            raise Exception("'position' in sensor configuration must be " \
                "integer ({} encountered)".format(type(position)))
        if position <= 0:
            raise Exception("'position' in sensor configuration must be " \
                "greater than zero".format(position))


def check_sensor_hardware(sensor):
    if 'hardware' in sensor:
        hardware = sensor['hardware']
        hw = zip(*settings.CHOOSE_SENSOR_HW)[0]
        if hardware not in hw:
            raise Exception("'hardware' in sensor configuration must be {} " \
                "({} encountered)".format(hw, hardware))


def check_sensor_pin(sensor, pin_name):
    if pin_name not in sensor:
        return
    pin = sensor[pin_name]
    if type(pin) not in six.integer_types:
        raise Exception("'{}' in sensor configuration must be " \
            "integer ({} encountered)".format(pin, type(pin)))
    if 'hardware' in sensor:
        # Safe to assume hardware has already been checked
        hardware = sensor['hardware']
        # Ignore test hardware as it has no pins and any existing pin
        # configuration should remain to avoid re-entry
        if hardware == settings.SENSOR_HW_TEST:
            return
        for n, hw in enumerate(settings.CHOOSE_SENSOR_HW):
            if hw[0] == hardware:
                pins = zip(*hw[2])[0]
                if pin not in pins:
                    raise Exception("'{}' in sensor configuration invalid " \
                        "for {} hardware, must be {} ({} encountered)".format(
                            pin_name, hardware, pins, pin))
    else:
        raise Exception("'hardware' in sensor configuration must be " \
            "specified if setting pin")


def check_laptimer(laptimer):
    """
    Check a laptimer configuration item.

    :param laptimer: The laptimer configuration to check.
    :type laptimer: dict
    """
    for key in laptimer:
        if key not in ['name', 'url', 'unitOfMeasurement', 'timezone']:
            raise Exception("Encountered unknown attribute '{}' in laptimer " \
                "configuration".format(key))

    check_name(laptimer, 'laptimer')
    check_url(laptimer, 'laptimer')
    check_unit_of_measurement(laptimer)
    check_timezone(laptimer)

    return laptimer


def check_sensor(sensor):
    """
    Check a sensor configuration item.

    :param sensor: The sensor configuration to check.
    :type sensor: dict
    """
    if type(sensor) != dict:
        raise Exception("Sensor items must be dictionaries ({} encountered)" \
            "\n\n{}".format(type(sensor), pformat(sensor)))

    for key in sensor:
        if key not in ['name', 'url', 'location', 'position', 'hardware',
        settings.SENSOR_PIN_LED_APP[0], settings.SENSOR_PIN_LED_HEARTBEAT[0],
        settings.SENSOR_PIN_LED_LAP[0], settings.SENSOR_PIN_LED_EVENT[0],
        settings.SENSOR_PIN_EVENT[0]]:
            raise Exception("Encountered unknown attribute '{}' in sensor " \
                "configuration".format(key))

    check_name(sensor, 'sensor')
    check_url(sensor, 'sensor')
    check_sensor_location(sensor)
    check_sensor_position(sensor)
    check_sensor_hardware(sensor)
    check_sensor_pin(sensor, settings.SENSOR_PIN_LED_APP[0])
    check_sensor_pin(sensor, settings.SENSOR_PIN_LED_HEARTBEAT[0])
    check_sensor_pin(sensor, settings.SENSOR_PIN_LED_LAP[0])
    check_sensor_pin(sensor, settings.SENSOR_PIN_LED_EVENT[0])
    check_sensor_pin(sensor, settings.SENSOR_PIN_EVENT[0])

    return sensor


def check_config(config):
    """
    Check a pi-time top-level configuration.

    :param config: The configuration to check.
    :type config: dict
    """

    if type(config) != dict:
        raise Exception(
            "Top-level configuration item must be a dictionary ({} " \
                "encountered)".format(type(config)))

    for k in config:
        if k not in ['laptimer', 'sensors']:
            raise Exception("Encountered unknown attribute '{}' in " \
                "top-level configuration".format(k))

    # check laptimer config
    if 'laptimer' in config:
        log.msg("Checking laptimer", logLevel=logging.DEBUG)
        check_laptimer(config['laptimer'])

    # check sensors config
    sensors = config.get('sensors', [])

    if type(sensors) != list:
        raise Exception("'sensors' attribute in top-level configuration must " \
            "be a list ({} encountered)".format(type(sensors)))

    i = 1
    for sensor in sensors:
        log.msg("Checking sensor item {}".format(i), logLevel=logging.DEBUG)
        check_sensor(sensor)
        i += 1


def check_config_file(config_file):
    """
    Check a pi-time configuration file.

    :param config_file: The file to check.
    :type config_file: str
    """
    log.msg('Checking configuration file {}'.format(config_file),
        logLevel=logging.DEBUG)

    configext = os.path.splitext(config_file)[1]
    config_file = os.path.abspath(config_file)

    with open(config_file, 'rb') as infile:
        try:
            config = json.load(infile)
        except ValueError as e:
            raise Exception("Configuration file '{}' does not seem to be proper " \
                "JSON ('{}')".format(config_file, e))

    check_config(config)

    return config
