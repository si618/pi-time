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
def add_lap_time(session_name, rider_name, sensor_name, time):
    '''Adds a new lap time.'''
    '''Depends on sensor type to determine if start, sector or finish time.'''
    '''Sends a broadcast message describing the lap time.'''
    # TODO: Role enforcement - sensor and admin only
    method = 'add_lap_time'
    try:
        check = api_utils.check_if_not_found(Session, method, session_name)
        if check != True:
            return check
        check = api_utils.check_if_not_found(Rider, method, rider_name)
        if check != True:
            return check
        check = api_utils.check_if_not_found(Sensor, method, sensor_name)
        if check != True:
            return check
        if time is None or type(time) is not datetime.datetime:
            error = 'Time must be valid datetime' # TODO: i18n
            return ApiResult(method, ok=False, data=error)
        session = Session.objects.get(name=session_name)
        rider = Rider.objects.get(name=rider_name)
        sensor = Sensor.objects.get(name=sensor_name)
        if sensor.sensor_type == settings.SENSOR_START:
            result = _add_lap_time_start(method, session, rider, sensor, time)
        elif sensor.sensor_type == settings.SENSOR_FINISH:
            result = _add_lap_time_finish(method, session, rider, sensor, time)
        elif sensor.sensor_type == settings.SENSOR_START_FINISH:
            result = _add_lap_time_start_finish(method, session, rider, sensor, 
                time)
        elif sensor.sensor_type == settings.SENSOR_SECTOR:
            result = _add_lap_time_sector(method, session, rider, sensor, time)
        else:
            error = 'Unknown sensor type: %s' % sensor_type # TODO: i18n
            result = ApiResult(method, ok=False, data=error)
        if result.ok:
            # TODO: Broadcast
            pass
        return result
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def remove_lap(session_name, rider_name, start_time):
    '''Deletes the lap. This is a soft delete and can be undone.'''
    '''Sends a broadcast message after lap has been removed.'''
    # TODO: Role enforcement - admins only
    method = 'remove_lap'
    try:
        check = api_utils.check_if_not_found(Session, method, session_name)
        if check != True:
            return check
        check = api_utils.check_if_not_found(Rider, method, rider_name)
        if check != True:
            return check
        session = Session.objects.get(name=session_name)
        rider = Rider.objects.get(name=rider_name)
        laps = Lap.objects.filter(session=session, rider=rider, \
            laptime__lap_start__eq=start_time)
        count = laps.count()
        laps.delete()
        logger.info('Removed laps for rider: %s in session %s:' \
            % (count, rider_name, session_name))
        return ApiResult(method, ok=True, data=laps)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def cancel_incomplete_laps(session_name, rider_name):
    '''Deletes all incomplete laps for the specified rider and session.'''
    '''Sends a broadcast message after laps have been cancelled.'''
    # TODO: Role enforcement - admin or current rider only
    method = 'cancel_incomplete_laps'
    try:
        check = api_utils.check_if_not_found(Session, method, session_name)
        if check != True:
            return check
        check = api_utils.check_if_not_found(Rider, method, rider_name)
        if check != True:
            return check
        session = Session.objects.get(name=session_name)
        rider = Rider.objects.get(name=rider_name)
        laps = Lap.objects.filter(session=session, rider=rider, \
            finish__isnull=True)
        count = laps.count()
        laps.delete()
        logger.info('Cancelled %s incomplete laps for rider: %s in session %s:' \
            % (count, rider_name, session_name))
        return ApiResult(method, ok=True, data=laps)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def get_incomplete_laps(track_name=None):
    '''Gets incomplete laps.'''
    method = 'get_incomplete_laps'
    try:
        data = 'TODO: Gets incomplete laps...'
        logger.info('%s: %s' % (method, data))
        return ApiResult(method, ok=True, data=data)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

# Private helper functions

def _add_lap_time_start(method, session, rider, sensor, time):
    if Lap.objects.filter(session=session, rider=rider, \
        finish__isnull=True).exists():
        error = 'Unable to start lap as an incomplete lap for rider %s in ' \
                'session %s already exists' % (rider.name, session.name) # TODO: i18n
        return ApiResult(method, ok=False, data=error)
    lap = Lap.objects.create(session=session, rider=rider)
    lap.save()
    lap_time = SensorEvent.objects.create(lap=lap, sensor=sensor, time=time)
    lap_time.save()
    lap.start = lap_time
    lap.save()
    logger.info('Lap started: %s rider: %s' % (timezone.localtime(time),
        rider.name))
    return ApiResult(method, ok=True, data=lap)

def _add_lap_time_finish(method, session, rider, sensor, time):
    if not Lap.objects.filter(session=session, rider=rider, \
        finish__isnull=True).exists():
        error = 'Unable to finish lap as no incomplete lap was found for ' \
                'rider %s in session %s' % (rider.name, session.name) # TODO: i18n
        return ApiResult(method, ok=False, data=error)
    laps = Lap.objects.filter(session=session, rider=rider, \
        finish__isnull=True)
    if laps.count() > 1:
        error = 'Unable to finish lap as more than one incomplete lap was ' \
                'found for rider %s in session %s' % (rider.name, session.name) # TODO: i18n
        return ApiResult(method, ok=False, data=error)
    lap = laps[0]
    lap_time = SensorEvent.objects.create(lap=lap, sensor=sensor, time=time)
    lap_time.save()
    lap.finish = lap_time
    lap.modified = timezone.now()
    lap.save()
    logger.info('Lap finished: %s rider: %s time: %s'
        % (timezone.localtime(time), rider.name, lap))
    return ApiResult(method, ok=True, data=lap)

def _add_lap_time_start_finish(method, session, rider, sensor, time):
    if Lap.objects.filter(session=session, rider=rider, \
        finish__isnull=True).exists():
        return _add_lap_time_finish(method, session, rider, sensor, time)
    else:
        return _add_lap_time_start(method, session, rider, sensor, time)

def _add_lap_time_sector(method, session, rider, sensor, time):
    error = 'Sector based sensors not currently supported'
    return ApiResult(method, ok=False, data=error)
