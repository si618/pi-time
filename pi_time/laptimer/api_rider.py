from autobahn.wamp1.protocol import exportRpc
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from laptimer import api_utils
from laptimer.models import ApiResult, \
                            ApiBroadcast, \
                            Rider
import datetime
import logging


logger = logging.getLogger('laptimer')

# API functions relating to riders

@exportRpc
def add_rider(rider_name):
    '''
    Adds a new rider.

    :param rider_name: Unique name of rider to be added.
    :type rider_name: str

    :authorization: Administrators.
    :broadcast: Administrators, riders and spectators.
    :returns: Details of added rider.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'add_rider'
    try:
        check = api_utils.check_if_found(Rider, method, rider_name)
        if check != True:
            return check
        rider = Rider.objects.create(name=rider_name)
        # TODO: Add rider as Django user in rider group
        logger.info('%s: %s' % (method, rider.name))
        result = ApiResult(method, ok=True, data=rider)
        # TODO: Broadcast result
        return result
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def change_rider(rider_name, new_rider_name):
    '''
    Changes the riders name.

    :param rider_name: Current name of rider.
    :type rider_name: str
    :param new_rider_name: New unique name of rider.
    :type new_rider_name: str

    :authorization: Administrators.
    :broadcast: Administrators, riders and spectators.
    :returns: Details of changed rider.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'change_rider'
    try:
        check = api_utils.check_if_found(Rider, method, new_rider_name)
        if check != True:
            return check
        check = api_utils.check_if_not_found(Rider, method, rider_name)
        if check != True:
            return check
        rider = Rider.objects.get(name=rider_name)
        rider.name = new_rider_name
        rider.save()
        logger.info('%s: %s' % (method, rider.name))
        result = ApiResult(method, ok=True, data=rider)
        # TODO: Broadcast result
        return result
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def remove_rider(rider_name):
    '''
    Removes a rider, including all track, session and lap data.

    :param rider_name: Name of rider to be removed.
    :type rider_name: str

    :authorization: Administrators.
    :broadcast: Administrators, riders and spectators.
    :returns: Details of removed rider.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'remove_rider'
    try:
        check = api_utils.check_if_not_found(Rider, method, rider_name)
        if check != True:
            return check
        rider = Rider.objects.get(name=rider_name)
        rider.delete()
        logger.info('%s: %s' % (method, rider_name))
        result = ApiResult(method, ok=True, data=rider_name)
        # TODO: Broadcast result
        return result
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def get_rider(rider_name):
    '''
    Gets a rider.

    :param rider_name: Name of rider.
    :type rider_name: str

    :authorization: Administrators, riders and spectators.
    :returns: Details of rider.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'get_rider'
    try:
        check = api_utils.check_if_not_found(Rider, method, rider_name)
        if check != True:
            return check
        rider = Rider.objects.get(name=rider_name)
        logger.info('%s: %s' % (method, rider_name))
        return ApiResult(method, ok=True, data=rider)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def get_riders():
    '''
    Gets all riders.

    :authorization: Administrators, riders and spectators.
    :returns: Details of riders.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'get_riders'
    try:
        riders = Rider.objects.all()
        logger.info('%s: %s' % (method, riders))
        return ApiResult(method, ok=True, data=riders)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def get_rider_statistics(track_name, rider_name):
    '''
    Gets statistics on a rider's completed laps for a track.

    :param track_name: Name of track.
    :type track_name: str
    :param rider_name: Name of rider.
    :type rider_name: str

    :authorization: Administrators, riders and spectators.
    :returns: Rider's statistics.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    pass

@exportRpc
def get_rider_session_statistics(track_name, session_name, rider_name):
    '''
    Gets statistics on a rider's completed laps for a session.

    :param track_name: Name of track.
    :type track_name: str
    :param session_name: Name of session. Must exist for track.
    :type session_name: str
    :param rider_name: Name of rider.
    :type rider_name: str

    :authorization: Administrators, riders and spectators.
    :returns: Rider's session statistics.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    pass

@exportRpc
def get_rider_lap_current(track_name, session_name, rider_name):
    '''
    Gets statistics on a rider's current lap.

    :param track_name: Name of track.
    :type track_name: str
    :param session_name: Name of session. Must exist for track.
    :type session_name: str
    :param rider_name: Name of rider.
    :type rider_name: str

    :authorization: Administrators, riders and spectators.
    :returns: Rider's current lap.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    pass

@exportRpc
def get_rider_lap_previous(track_name, session_name, rider_name):
    '''
    Gets statistics on a riders previous lap.

    :param track_name: Name of track.
    :type track_name: str
    :param session_name: Name of session. Must exist for track.
    :type session_name: str
    :param rider_name: Name of rider.
    :type rider_name: str

    :authorization: Administrators, riders and spectators.
    :returns: Rider's previous lap.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    pass
