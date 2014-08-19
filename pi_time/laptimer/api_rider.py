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
    '''Add a new rider. Rider name must be unique.'''
    '''Sends a broadcast message after rider has been added.'''
    method = 'add_rider'
    try:
        check = api_utils.check_if_found(Rider, method, rider_name)
        if check != True:
            return check
        rider = Rider.objects.create(name=rider_name)
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
    '''Changes the riders name. Rider name must be unique.'''
    '''Sends a broadcast message after rider has been changed.'''
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
        rider.modified = timezone.now()
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
    '''Removes a rider, including all track, session and lap data.'''
    '''Sends a broadcast message after rider has been removed.'''
    # TODO: Role enforcement - admins only or current user matches rider_name
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
    '''Gets specified rider.'''
    # TODO: Role enforcement - admins, riders or spectators
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
    '''Gets all riders.'''
    # TODO: Role enforcement - admins, riders or spectators
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
def get_rider_laps(rider_name):
    '''Gets statistics on a riders completed laps for all tracks.'''
    # TODO: Role enforcement - admins, riders or spectators
    pass

@exportRpc
def get_rider_laps_for_track(rider_name, track_name):
    '''Gets statistics on a riders completed laps for a track.'''
    # TODO: Role enforcement - admins, riders or spectators
    pass

@exportRpc
def get_rider_track_record(rider_name, track_name):
    '''Gets statistics on a riders lap record for a track.'''
    # TODO: Role enforcement - admins, riders or spectators
    pass

@exportRpc
def get_rider_track_average(rider_name, track_name):
    '''Gets statistics on a riders lap average for a track.'''
    # TODO: Role enforcement - admins, riders or spectators
    pass

@exportRpc
def get_rider_session_laps(rider_name, session_name):
    '''Gets statistics on a riders completed laps for a session.'''
    # TODO: Role enforcement - admins, riders or spectators
    pass

@exportRpc
def get_rider_session_record(rider_name, session_name):
    '''Gets statistics on a riders lap record for a session.'''
    # TODO: Role enforcement - admins, riders or spectators
    pass

@exportRpc
def get_rider_session_average(rider_name, session_name):
    '''Gets statistics on a riders lap average for a session.'''
    # TODO: Role enforcement - admins, riders or spectators
    pass

@exportRpc
def get_rider_lap_current(rider_name, session_name):
    '''Gets statistics on a riders current lap.'''
    # TODO: Role enforcement - admins, riders or spectators
    pass

@exportRpc
def get_rider_lap_previous(rider_name, session_name):
    '''Gets statistics on a riders previous lap.'''
    # TODO: Role enforcement - admins, riders or spectators
    pass
