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

# API functions relating to sensor events

@exportRpc
def add_sensor_event(track_name, session_name, rider_name, sensor_name, time):
    '''
    Adds a new sensor event.

    Depends on sensor position to determine if start, sector or finish time.

    :param track_name: Name of track.
    :type track_name: str
    :param session_name: Name of session. Must exist for track.
    :type session_name: str
    :param rider_name: Name of rider.
    :type rider_name: str
    :param sensor_name: Name of sensor. Must exist for track.
    :type sensor_name: str
    :param time: Local time of sensor event.
    :type time: datetime

    :authorization: Administrators and sensors.
    :broadcast: Administrators, riders, spectators and sensors.
    :returns: Details of sensor event.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'add_sensor_event'
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
        check = api_utils.check_if_not_found(Sensor, method, sensor_name)
        if check != True:
            return check
        if time is None or type(time) is not datetime.datetime:
            error = 'Time must be valid datetime' # TODO: i18n
            return ApiResult(method, ok=False, data=error)
        session = Session.objects.get(name=session_name,
            track__name=track_name)
        rider = Rider.objects.get(name=rider_name)
        sensor = Sensor.objects.get(track__name=track_name, name=sensor_name)
        if sensor.sensor_pos == settings.SENSOR_POS_START:
            result = _add_sensor_event_start(method, session, rider, sensor, time)
        elif sensor.sensor_pos == settings.SENSOR_POS_FINISH:
            result = _add_sensor_event_finish(method, session, rider, sensor, time)
        elif sensor.sensor_pos == settings.SENSOR_POS_START_FINISH:
            result = _add_sensor_event_start_finish(method, session, rider, sensor,
                time)
        elif sensor.sensor_pos == settings.SENSOR_POS_SECTOR:
            result = _add_sensor_event_sector(method, session, rider, sensor, time)
        else:
            error = 'Unknown sensor position: %s' % sensor_pos # TODO: i18n
            result = ApiResult(method, ok=False, data=error)
        if result.ok:
            # TODO: Broadcast
            pass
        return result
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

# Private helper functions

def _add_sensor_event_start(method, session, rider, sensor, time):
    if Lap.objects.filter(session=session, rider=rider, \
        finish__isnull=True).exists():
        error = 'Unable to start lap as an incomplete lap for rider %s in ' \
                'session %s already exists' % (rider.name, session.name) # TODO: i18n
        return ApiResult(method, ok=False, data=error)
    lap = Lap.objects.create(session=session, rider=rider)
    lap.save()
    sensor_event = SensorEvent.objects.create(lap=lap, sensor=sensor,
        time=time)
    sensor_event.save()
    lap.start = sensor_event
    lap.save()
    logger.info('Lap started: %s rider: %s' % (timezone.localtime(time),
        rider.name))
    return ApiResult(method, ok=True, data=lap)

def _add_sensor_event_finish(method, session, rider, sensor, time):
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
    sensor_event = SensorEvent.objects.create(lap=lap, sensor=sensor,
        time=time)
    sensor_event.save()
    lap.finish = sensor_event
    lap.save()
    logger.info('Lap finished: %s rider: %s time: %s'
        % (timezone.localtime(time), rider.name, lap))
    return ApiResult(method, ok=True, data=lap)

def _add_sensor_event_start_finish(method, session, rider, sensor, time):
    if Lap.objects.filter(session=session, rider=rider, \
        finish__isnull=True).exists():
        return _add_sensor_event_finish(method, session, rider, sensor, time)
    else:
        return _add_sensor_event_start(method, session, rider, sensor, time)

def _add_sensor_event_sector(method, session, rider, sensor, time):
    error = 'Sector based sensors not currently supported'
    return ApiResult(method, ok=False, data=error)
