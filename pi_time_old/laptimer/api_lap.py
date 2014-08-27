from autobahn.wamp1.protocol import exportRpc
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from laptimer import api_utils
from laptimer.models import ApiResult, \
                            ApiBroadcast, \
                            Lap, \
                            Rider, \
                            Session, \
                            Sensor, \
                            SensorEvent, \
                            Track
import datetime
import logging


logger = logging.getLogger('laptimer')

# API functions relating to laps

@exportRpc
def change_rider_for_lap(track_name, session_name, rider_name, start_time,
    new_rider_name):
    '''
    Changes the rider associated with a lap and its sensor events.

    :param track_name: Name of track.
    :type track_name: str
    :param session_name: Name of session. Must exist for track.
    :type session_name: str
    :param rider_name: Name of current rider for lap.
    :type rider_name: str
    :param start_time: Start time of lap.
    :type time: datetime
    :param new_rider_name: Name of new rider for lap.
    :type new_rider_name: str

    :authorization: Administrators.
    :broadcast: Administrators, riders and spectators.
    :returns: Details of changed lap.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'change_rider_for_lap'
    try:
        check = api_utils.check_if_not_found(Track, method, track_name)
        if check != True:
            return check
        check = api_utils.check_if_not_found(Session, method, session_name)
        if check != True:
            return check
        check = api_utils.check_if_not_found(Rider, method, rider_name)
        if check != True:
            return check
        check = api_utils.check_if_not_found(Rider, method, new_rider_name)
        if check != True:
            return check
        session = Session.objects.get(name=session_name,
            track__name=track_name)
        rider = Rider.objects.get(name=rider_name)
        new_rider = Rider.objects.get(name=new_rider_name)
        lap = Lap.objects.get(session=session, rider=rider, \
            start__time=start_time)
        lap.rider = new_rider
        lap.save()
        logger.info(
            'Changed rider for lap starting: %s from: %s to: %s in session: %s' \
            % (start_time, rider_name, new_rider_name, session_name))
        return ApiResult(method, ok=True, data=lap)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def remove_lap(track_name, session_name, rider_name, start_time):
    '''
    Removes a lap and associated sensor events.

    :param track_name: Name of track.
    :type track_name: str
    :param session_name: Name of session. Must exist for track.
    :type session_name: str
    :param rider_name: Name of rider.
    :type rider_name: str
    :param start_time: Start time of lap.
    :type time: datetime

    :authorization: Administrators.
    :broadcast: Administrators, riders and spectators.
    :returns: Details of removed lap.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'remove_lap'
    try:
        check = api_utils.check_if_not_found(Track, method, track_name)
        if check != True:
            return check
        check = api_utils.check_if_not_found(Session, method, session_name)
        if check != True:
            return check
        check = api_utils.check_if_not_found(Rider, method, rider_name)
        if check != True:
            return check
        session = Session.objects.get(name=session_name,
            track__name=track_name)
        rider = Rider.objects.get(name=rider_name)
        lap = Lap.objects.get(session=session, rider=rider, \
            start__time=start_time)
        lap.delete()
        events = SensorEvent.objects.filter(lap=lap)
        events.delete()
        logger.info('Removed lap starting: %s for rider: %s in session: %s' \
            % (start_time, rider_name, session_name))
        return ApiResult(method, ok=True, data=lap)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def remove_incomplete_laps(track_name, session_name, rider_name):
    '''
    Removes incomplete laps.

    :param track_name: Name of track.
    :type track_name: str
    :param session_name: Name of session. Must exist for track.
    :type session_name: str
    :param rider_name: Name of rider.
    :type rider_name: str

    :authorization: Administrators.
    :broadcast: Administrators, riders, spectators and sensors.
    :returns: Details of incomplete laps removed.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    # TODO: Role enforcement - admin or current rider only
    method = 'remove_incomplete_laps'
    try:
        check = api_utils.check_if_not_found(Track, method, track_name)
        if check != True:
            return check
        check = api_utils.check_if_not_found(Session, method, session_name)
        if check != True:
            return check
        check = api_utils.check_if_not_found(Rider, method, rider_name)
        if check != True:
            return check
        session = Session.objects.get(name=session_name,
            track__name=track_name)
        rider = Rider.objects.get(name=rider_name)
        laps = Lap.objects.filter(session=session, rider=rider, \
            finish__isnull=True)
        count = laps.count()
        laps.delete()
        logger.info(
            'Cancelled %s incomplete laps for rider: %s in session: %s' \
            % (count, rider_name, session_name))
        return ApiResult(method, ok=True, data=laps)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def get_incomplete_laps(track_name, session_name):
    '''
    Gets incomplete laps for a track session.

    :param track_name: Name of track.
    :type track_name: str
    :param session_name: Name of session. Must exist for track.
    :type session_name: str

    :authorization: Administrators, riders and spectators.
    :returns: Details of incomplete laps.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'get_incomplete_laps'
    try:
        check = api_utils.check_if_not_found(Track, method, track_name)
        if check != True:
            return check
        check = api_utils.check_if_not_found(Session, method, session_name)
        if check != True:
            return check
        session = Session.objects.get(name=session_name,
            track__name=track_name)
        laps = Lap.objects.filter(session=session, finish__isnull=True)
        logger.info('%s: %s' % (method, data))
        return ApiResult(method, ok=True, data=laps)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)
