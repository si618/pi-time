from django.conf import settings
from django.db import transaction
from django.utils import timezone
from laptimer.models import APIResult, APIBroadcast, Lap, LapTime, Rider, Session, Sensor, Track
import datetime
import logging


logger = logging.getLogger('laptimer')

'''Interface for client communication with a lap timer server.'''

# Rider methods

def add_rider(rider_name):
    '''Add a new rider. Rider name must be unique.'''
    '''Sends a broadcast message after rider has been added.'''
    method = 'add_rider'
    try:
        check = _check_if_found(Rider, method, rider_name)
        if check != True:
            return check
        rider = Rider.objects.create(name=rider_name)
        logger.info('%s: %s' % (method, rider.name))
        return APIResult(method, successful=True, data=rider)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return APIResult(method, successful=False, data=error)

def change_rider(rider_name, new_rider_name):
    '''Changes the riders name. Rider name must be unique.'''
    '''Sends a broadcast message after rider has been changed.'''
    method = 'change_rider'
    try:
        check = _check_if_found(Rider, method, new_rider_name)
        if check != True:
            return check
        check = _check_if_not_found(Rider, method, rider_name)
        if check != True:
            return check
        rider = Rider.objects.get(name=rider_name)
        rider.name = new_rider_name
        rider.modified = timezone.now()
        rider.save()
        logger.info('%s: %s' % (method, rider.name))
        return APIResult(method, successful=True, data=rider)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return APIResult(method, successful=False, data=error)

def remove_rider(rider_name):
    '''Removes a rider, including all track, session and lap data.'''
    '''Sends a broadcast message after rider has been removed.'''
    # TODO: Role enforcement - admins only
    method = 'remove_rider'
    try:
        check = _check_if_not_found(Rider, method, rider_name)
        if check != True:
            return check
        rider = Rider.objects.get(name=rider_name)
        rider.delete()
        logger.info('%s: %s' % (method, rider_name))
        return APIResult(method, successful=True, data=rider_name)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return APIResult(method, successful=False, data=error)

def get_rider_laps(rider_name):
    '''Gets statistics on a riders completed laps for all tracks.'''
    pass

def get_rider_track_laps(rider_name, track_name):
    '''Gets statistics on a riders completed laps for a track.'''
    pass

def get_rider_track_record(rider_name, track_name):
    '''Gets statistics on a riders lap record for a track.'''
    pass

def get_rider_track_average(rider_name, track_name):
    '''Gets statistics on a riders lap average for a track.'''
    pass

def get_rider_session_laps(rider_name, session_name):
    '''Gets statistics on a riders completed laps for a session.'''
    pass

def get_rider_session_record(rider_name, session_name):
    '''Gets statistics on a riders lap record for a session.'''
    pass

def get_rider_session_average(rider_name, session_name):
    '''Gets statistics on a riders lap average for a session.'''
    pass

def get_rider_lap_current(rider_name, session_name):
    '''Gets statistics on a riders current lap.'''
    pass

def get_rider_lap_previous(rider_name, session_name):
    '''Gets statistics on a riders previous lap.'''
    pass


# Track methods

def add_track(track_name, track_distance, lap_timeout,
    unit_of_measurement):
    '''Add a new track. Track name must be unique.'''
    '''Sends a broadcast message after track has been added.'''
    # TODO: Role enforcement - admins only
    method = 'add_track'
    try:
        check = _check_if_found(Track, method, track_name)
        if check != True:
            return check
        if unit_of_measurement not in dict(settings.UNIT_OF_MEASUREMENT):
            error = 'Invalid unit of measurement' # TODO: i18n
            return APIResult(method, successful=False, data=error)
        track = Track.objects.create(name=track_name,
            distance=track_distance, timeout=lap_timeout,
            unit_of_measurement=unit_of_measurement)
        logger.info('%s: %s' % (method, track.name))
        return APIResult(method, successful=True, data=track)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return APIResult(method, successful=False, data=error)

def change_track(track_name, new_track_name=None, new_track_distance=None,
    new_lap_timeout=None, new_unit_of_measurement=None):
    '''Changes track details. Track name must be unique.'''
    '''Sends a broadcast message after track has been changed.'''
    # TODO: Role enforcement - admins only
    method = 'change_track'
    try:
        check = _check_if_not_found(Track, method, track_name)
        if check != True:
            return check
        if new_track_name == None and new_track_distance == None \
        and new_lap_timeout == None and new_unit_of_measurement == None:
            error = 'At least one new track detail is required' # TODO: i18n
            return APIResult(method, successful=False, data=error)
        if new_unit_of_measurement != None \
        and new_unit_of_measurement not in dict(settings.UNIT_OF_MEASUREMENT):
            error = 'Invalid unit of measurement' # TODO: i18n
            return APIResult(method, successful=False, data=error)
        if new_track_name != None:
            check = _check_if_found(Track, method, new_track_name)
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
        track.modified = timezone.now()
        track.save()
        logger.info('%s: %s' % (method, track.name))
        return APIResult(method, successful=True, data=track)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return APIResult(method, successful=False, data=error)

def remove_track(track_name):
    '''Removes a track, including all session and lap data.'''
    '''Sends a broadcast message after track has been removed.'''
    # TODO: Role enforcement - admins only
    method = 'remove_track'
    try:
        check = _check_if_not_found(Track, method, track_name)
        if check != True:
            return check
        track = Track.objects.get(name=track_name)
        track.delete()
        logger.info('%s: %s' % (method, track_name))
        return APIResult(method, successful=True, data=track_name)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return APIResult(method, successful=False, data=error)

def get_track_statistics(track_name):
    '''Gets all track statistics.'''
    pass

def get_track_lap_record(track_name):
    '''Gets statistics on track lap record.'''
    pass

def get_track_lap_average(track_name):
    '''Gets statistics on track lap average.'''
    pass


# Session methods

def add_session(track_name, session_name):
    '''Adds a new session. Session name must be unique for all tracks.'''
    '''Sends a broadcast message after session has been added.'''
    # TODO: Role enforcement - admins only
    method = 'add_session'
    try:
        trackCheck = _check_if_not_found(Track, method, track_name)
        if trackCheck != True:
            return trackCheck
        sessionCheck = _check_if_found(Session, method, session_name)
        if sessionCheck != True:
            return sessionCheck
        track = Track.objects.get(name=track_name)
        session = Session.objects.create(track_id=track.id, name=session_name)
        logger.info('%s: %s' % (method, session.name))
        return APIResult(method, successful=True, data=session)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return APIResult(method, successful=False, data=error)

def change_session(session_name, new_session_name=None, new_track_name=None):
    '''Changes the session.'''
    '''Sends a broadcast message after session has been changed.'''
    # TODO: Role enforcement - admins only
    method = 'change_session'
    try:
        check = _check_if_not_found(Session, method, session_name)
        if check != True:
            return check
        if new_session_name == None and new_track_name == None:
            error = 'New session or track name is required' # TODO: i18n
            return APIResult(method, successful=False, data=error)
        if new_session_name != None:
            check = _check_if_found(Session, method, new_session_name)
            if check != True:
                return check
        if new_track_name != None:
            check = _check_if_not_found(Track, method, new_track_name)
            if check != True:
                return check
        session = Session.objects.get(name=session_name)
        if new_session_name != None:
            session.name = new_session_name
        if new_track_name != None:
            session.track = Track.objects.get(name=new_track_name)
        session.modified = timezone.now()
        session.save()
        logger.info('%s: %s' % (method, session.name))
        return APIResult(method, successful=True, data=session)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return APIResult(method, successful=False, data=error)

def remove_session(session_name):
    '''Removes a session, including all lap data.'''
    '''Sends a broadcast message after session has been removed.'''
    # TODO: Role enforcement - admins only
    method = 'remove_session'
    try:
        check = _check_if_not_found(Session, method, session_name)
        if check != True:
            return check
        session = Session.objects.get(name=session_name)
        session.delete()
        logger.info('%s: %s' % (method, session_name))
        return APIResult(method, successful=True, data=session_name)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return APIResult(method, successful=False, data=error)

def get_session_statistics(session_name):
    '''Gets all session statistics.'''

def get_session_lap_record(session_name):
    '''Gets statistics on session lap record.'''
    pass

def get_session_lap_average(session_name):
    '''Gets statistics on session lap average.'''
    pass


# Lap methods

def add_lap_time(session_name, rider_name, sensor_name, time):
    '''Adds a new lap time.'''
    '''Depends on sensor type to determine if start, sector or finish time.'''
    '''Sends a broadcast message describing the lap time.'''
    # TODO: Role enforcement - sensor and admin only
    method = 'add_lap_time'
    try:
        check = _check_if_not_found(Session, method, session_name)
        if check != True:
            return check
        check = _check_if_not_found(Rider, method, rider_name)
        if check != True:
            return check
        check = _check_if_not_found(Sensor, method, sensor_name)
        if check != True:
            return check
        if time is None or type(time) is not datetime.datetime:
            error = 'Time must be valid datetime' # TODO: i18n
            return APIResult(method, successful=False, data=error)
        session = Session.objects.get(name=session_name)
        rider = Rider.objects.get(name=rider_name)
        sensor = Sensor.objects.get(name=sensor_name)
        if sensor.sensor_type == settings.SENSOR_START:
            return _add_lap_time_start(method, session, rider, sensor, time)
        elif sensor.sensor_type == settings.SENSOR_FINISH:
            return _add_lap_time_finish(method, session, rider, sensor, time)
        elif sensor.sensor_type == settings.SENSOR_START_FINISH:
            return _add_lap_time_start_finish(method, session, rider, sensor, time)
        elif sensor.sensor_type == settings.SENSOR_SECTOR:
            return _add_lap_time_sector(method, session, rider, sensor, time)
        else:
            error = 'Unknown sensor type: %s' % sensor_type # TODO: i18n
            return APIResult(method, successful=False, data=error)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return APIResult(method, successful=False, data=error)

def _add_lap_time_start(method, session, rider, sensor, time):
    if Lap.objects.filter(session=session, rider=rider, \
        finish__isnull=True).exists():
        error = 'Unable to start lap as an incomplete lap for rider %s in ' \
                'session %s already exists' % (rider.name, session.name) # TODO: i18n
        return APIResult(method, successful=False, data=error)
    lap = Lap.objects.create(session=session, rider=rider)
    lap.save()
    lap_time = LapTime.objects.create(lap=lap, sensor=sensor, time=time)
    lap_time.save()
    lap.start = lap_time
    lap.save()
    logger.info('Lap started: %s rider: %s' % (timezone.localtime(time),
        rider.name))
    return APIResult(method, successful=True, data=lap)

def _add_lap_time_finish(method, session, rider, sensor, time):
    if not Lap.objects.filter(session=session, rider=rider, \
        finish__isnull=True).exists():
        error = 'Unable to finish lap as no incomplete lap was found for ' \
                'rider %s in session %s' % (rider.name, session.name) # TODO: i18n
        return APIResult(method, successful=False, data=error)
    laps = Lap.objects.filter(session=session, rider=rider, \
        finish__isnull=True)
    if laps.count() > 1:
        error = 'Unable to finish lap as more than one incomplete lap was ' \
                'found for rider %s in session %s' % (rider.name, session.name) # TODO: i18n
        return APIResult(method, successful=False, data=error)
    lap = laps[0]
    lap_time = LapTime.objects.create(lap=lap, sensor=sensor, time=time)
    lap_time.save()
    lap.finish = lap_time
    lap.modified = timezone.now()
    lap.save()
    logger.info('Lap finished: %s rider: %s time: %s'
        % (timezone.localtime(time), rider.name, lap))
    return APIResult(method, successful=True, data=lap)

def _add_lap_time_start_finish(method, session, rider, sensor, time):
    if Lap.objects.filter(session=session, rider=rider, \
        finish__isnull=True).exists():
        return _add_lap_time_finish(method, session, rider, sensor, time)
    else:
        return _add_lap_time_start(method, session, rider, sensor, time)

def _add_lap_time_sector(method, session, rider, sensor, time):
    error = 'Sector based sensors not currently supported'
    return APIResult(method, successful=False, data=error)

def cancel_incomplete_laps(session_name, rider_name):
    '''Deletes all incomplete laps for the specified rider and session.'''
    '''Sends a broadcast message after laps have been cancelled.'''
    # TODO: Role enforcement - admin or current rider only
    method = 'cancel_incomplete_laps'
    try:
        check = _check_if_not_found(Session, method, session_name)
        if check != True:
            return check
        check = _check_if_not_found(Rider, method, rider_name)
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
        return APIResult(method, successful=True, data=laps)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return APIResult(method, successful=False, data=error)

def remove_lap(session_name, rider_name, start_time):
    '''Deletes the lap. This is a soft delete and can be undone.'''
    '''Sends a broadcast message after lap has been removed.'''
    # TODO: Role enforcement - admins only
    method = 'remove_lap'
    try:
        check = _check_if_not_found(Session, method, session_name)
        if check != True:
            return check
        check = _check_if_not_found(Rider, method, rider_name)
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
        return APIResult(method, successful=True, data=laps)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return APIResult(method, successful=False, data=error)


# General methods

def server_poweroff(reboot=False):
    '''Powers off the server after cancelling any unfinished laps.'''
    '''Invokes method: get_unfinished_laps and then cancel_lap.'''
    '''Sends a broadcast message before server is powered off.'''
    # TODO: Role enforcement - admins only
    pass

def backup_to_cloud(modified=None):
    '''If modified specified, only data on or after this time is backed up.'''
    # TODO: Role enforcement - admins only
    return APIResult('backup_to_cloud', successful=True, data='Cloud info goes here...')

def get_data(modified=None):
    '''Gets track, session, rider, lap data and settings. Useful for backup.'''
    '''If modified is specified, only data on or after this time is returned.'''
    return APIResult('get_data', successful=True, data='Data goes here...')

def get_unfinished_laps(track_name=None):
    '''Gets unfinished laps.'''
    pass


# Helper methods

def _check_if_found(calling_object, calling_method, name):
    if calling_object.objects.filter(name=name).exists():
        error = '%s already exists' % calling_object.__name__ # TODO: i18n
        return APIResult(calling_method, successful=False, data=error)
    return True

def _check_if_not_found(calling_object, calling_method, name):
    if not calling_object.objects.filter(name=name).exists():
        error = '%s not found' % calling_object.__name__ # TODO: i18n
        return APIResult(calling_method, successful=False, data=error)
    return True
