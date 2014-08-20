from autobahn.wamp1.protocol import exportRpc
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from laptimer import api_utils
from laptimer.models import ApiResult, \
                            ApiBroadcast, \
                            Track
import logging


logger = logging.getLogger('laptimer')

# API functions relating to tracks

@exportRpc
def add_track(track_name, track_distance, lap_timeout,
    unit_of_measurement):
    '''
    Add a new track.

    :param track_name: Unique name of track.
    :type track_name: str
    :param track_distance: Total track distance.
    :type track_distance: float
    :param lap_timeout: Maximum number of seconds before a lap times out.
    :type lap_timeout: integer
    :param unit_of_measurement: Unit of measurement, either Metric or Imperial.
    :type unit_of_measurement: str

    :authorization: Administrators.
    :broadcast: Administrators, riders and spectators.
    :returns: Details of new track.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    # TODO: Role enforcement - admins only
    method = 'add_track'
    try:
        check = api_utils.check_if_found(Track, method, track_name)
        if check != True:
            return check
        if unit_of_measurement not in dict(settings.UNIT_OF_MEASUREMENT):
            error = 'Invalid unit of measurement' # TODO: i18n
            return ApiResult(method, ok=False, data=error)
        track = Track.objects.create(name=track_name,
            distance=track_distance, timeout=lap_timeout,
            unit_of_measurement=unit_of_measurement)
        logger.info('%s: %s' % (method, track.name))
        result = ApiResult(method, ok=True, data=track)
        # TODO: Broadcast result
        return result
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def change_track(track_name, new_track_name=None, new_track_distance=None,
    new_lap_timeout=None, new_unit_of_measurement=None):
    '''
    Changes track details.

    :param track_name: Current name of track.
    :type track_name: str
    :param new_track_name: New unique name of track.
    :type new_track_name: str
    :param new_track_distance: Total track distance.
    :type new_track_distance: float
    :param new_lap_timeout: Maximum number of seconds before a lap times out..
    :type new_lap_timeout: integer
    :param new_unit_of_measurement: Unit of measurement, either Metric or
    Imperial.
    :type new_unit_of_measurement: str

    :authorization: Administrators.
    :broadcast: Administrators, riders and spectators.
    :returns: Details of changed track.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'change_track'
    try:
        check = api_utils.check_if_not_found(Track, method, track_name)
        if check != True:
            return check
        if new_track_name == None and new_track_distance == None \
        and new_lap_timeout == None and new_unit_of_measurement == None:
            error = 'At least one new track detail is required' # TODO: i18n
            return ApiResult(method, ok=False, data=error)
        if new_unit_of_measurement != None \
        and new_unit_of_measurement not in dict(settings.UNIT_OF_MEASUREMENT):
            error = 'Invalid unit of measurement' # TODO: i18n
            return ApiResult(method, ok=False, data=error)
        if new_track_name != None:
            check = api_utils.check_if_found(Track, method, new_track_name)
            if check != True:
                return check
        track = Track.objects.get(name=track_name)
        if new_track_name != None:
            track.name = new_track_name
        if new_track_distance != None:
            track.distance = new_track_distance
        if new_lap_timeout != None:
            track.timeout = new_lap_timeout
        if new_unit_of_measurement != None:
            track.unit_of_measurement = new_unit_of_measurement
        track.save()
        logger.info('%s: %s' % (method, track.name))
        result = ApiResult(method, ok=True, data=track)
        # TODO: Broadcast result
        return result
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def remove_track(track_name):
    '''
    Removes a track, including all session and lap data.

    :param track_name: Name of track.
    :type track_name: str

    :authorization: Administrators.
    :broadcast: Administrators, riders and spectators.
    :returns: Details of removed track.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'remove_track'
    try:
        check = api_utils.check_if_not_found(Track, method, track_name)
        if check != True:
            return check
        track = Track.objects.get(name=track_name)
        track.delete()
        logger.info('%s: %s' % (method, track_name))
        result = ApiResult(method, ok=True, data=track_name)
        # TODO: Broadcast result
        return result
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def get_track(track_name):
    '''
    Gets a track.

    :param track_name: Name of track.
    :type track_name: str

    :authorization: Administrators, riders and spectators.
    :returns: Details of track.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'get_track'
    try:
        check = api_utils.check_if_not_found(Track, method, track_name)
        if check != True:
            return check
        track = Track.objects.get(name=track_name)
        logger.info('%s: %s' % (method, track_name))
        return ApiResult(method, ok=True, data=track)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def get_tracks():
    '''
    Gets all tracks.

    :authorization: Administrators, riders and spectators.
    :returns: Details of all tracks.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'get_tracks'
    try:
        tracks = Track.objects.all()
        logger.info('%s: %s' % (method, tracks))
        return ApiResult(method, ok=True, data=tracks)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def get_track_statistics(track_name):
    '''
    Gets statistics for a track.

    :param track_name: Name of track.
    :type track_name: str

    :authorization: Administrators, riders and spectators.
    :returns: Track statistics.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    pass
