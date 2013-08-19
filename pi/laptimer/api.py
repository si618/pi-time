from django.conf import settings
from django.db import transaction
from laptimer.models import APIResult, APIBroadcast, Track, Rider, Session, Lap
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
        return APIResult(method, result=True, data=rider)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return APIResult(method, result=False, data=error)

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
        rider.save()
        logger.info('%s: %s' % (method, rider.name))
        return APIResult(method, result=True, data=rider)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return APIResult(method, result=False, data=error)

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
        return APIResult(method, result=True, data=rider_name)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return APIResult('remove_rider', result=False, data=error)


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
            return APIResult(method, result=False, data=error)
        track = Track.objects.create(name=track_name,
            distance=track_distance, timeout=lap_timeout,
            unit_of_measurement=unit_of_measurement)
        logger.info('%s: %s' % (method, track.name))
        return APIResult(method, result=True, data=track)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return APIResult(method, result=False, data=error)

def change_track(track_name, track_distance, lap_timeout,
    unit_of_measurement):
    '''Changes the track details. Track name must be unique.'''
    '''Sends a broadcast message after track has been changed.'''
    # TODO: Role enforcement - admins only
    pass

def remove_track(track_name):
    '''Removes a track, including all session and lap data.'''
    '''Sends a broadcast message after track has been removed.'''
    # TODO: Role enforcement - admins only
    pass

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

def add_session(track_name, session_name, started=None):
    '''Adds and optionally starts a new session. Session name must be unique.'''
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
        session = Session.objects.create(track_id=track.id, name=session_name,
            start=started)
        logger.info('%s: %s' % (method, session.name))
        return APIResult(method, result=True, data=session)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return APIResult(method, result=False, data=error)
    pass

def change_session(session_name, new_session_name=None,
    new_track_name=None, new_start_time=None, new_end_time=None):
    '''Changes the session.'''
    '''Sends a broadcast message after session has been changed.'''
    # TODO: Role enforcement - admins only
    pass

def remove_session(session_name):
    '''Removes a session, including all lap data.'''
    '''Sends a broadcast message after session has been removed.'''
    # TODO: Role enforcement - admins only
    pass

def start_session(session_name, started):
    '''Starts a session.'''
    '''Sends a broadcast message after session has started.'''
    # TODO: Role enforcement - admins only
    pass

def end_session(session_name, end_time):
    '''Ends the session.'''
    '''Sends a broadcast message after session has ended.'''
    # TODO: Role enforcement - admins only
    pass

def get_session_statistics(session_name):
    '''Gets all session statistics.'''

def get_session_lap_record(session_name):
    '''Gets statistics on session lap record.'''
    pass

def get_session_lap_average(session_name):
    '''Gets statistics on session lap average.'''
    pass


# Lap methods

def start_lap(session_name, rider_name, start_time):
    '''Starts a new lap.'''
    '''Sends a broadcast message after lap has started.'''
    # TODO: Role enforcement - sensor only
    pass

def end_lap(session_name, rider_name, end_time):
    '''
    Ends the lap, starting a new lap using the end time as new start time.
    Sends a broadcast message after lap has ended.
    '''
    # TODO: Role enforcement - sensor only
    pass

def cancel_lap(session_name, rider_name, start_time):
    '''Cancels the current lap.'''
    '''Sends a broadcast message after lap has been cancelled.'''
    # TODO: Role enforcement - only admin or current rider
    pass

def remove_lap(session_name, rider_name, start_time):
    '''Removes the lap. This is a soft delete and can be undone.'''
    '''Sends a broadcast message after lap has been removed.'''
    # TODO: Role enforcement - admins only
    pass


# General methods

def server_poweroff(reboot=False):
    '''Powers off the server after cancelling any unfinished laps.'''
    '''Invokes method: get_unfinished_laps and then cancel_lap.'''
    '''Sends a broadcast message before server is powered off.'''
    # TODO: Role enforcement - admins only
    pass

def get_data(modified=None):
    '''
    Gets track, session, rider, lap data and settings. Useful for backup.
    If modified is specified, only data on or after this time is returned.
    '''
    return APIResult('get_data', result=True, data='Data goes here...')

def get_unfinished_laps(track_name=None):
    '''Gets unfinished laps.'''
    pass


# Helper methods

def _check_if_found(calling_object, calling_method, name):
    if calling_object.objects.filter(name=name).exists():
        error = '%s already exists' % calling_object.__name__ # TODO: i18n
        return APIResult(calling_method, result=False, data=error)
    return True

def _check_if_not_found(calling_object, calling_method, name):
    if not calling_object.objects.filter(name=name).exists():
        error = '%s not found' % calling_object.__name__ # TODO: i18n
        return APIResult(calling_method, result=False, data=error)
    return True
