from autobahn.wamp1.protocol import exportRpc
from django.utils import timezone
from laptimer import api_utils
from laptimer.models import ApiResult, \
                            ApiBroadcast, \
                            Session, \
                            Track
import logging


logger = logging.getLogger('laptimer')

# API functions relating to track sessions

@exportRpc
def add_session(track_name, session_name):
    '''Adds a new session. Session name must be unique for all tracks.'''
    '''Sends a broadcast message after session has been added.'''
    # TODO: Role enforcement - admins only
    method = 'add_session'
    try:
        trackCheck = api_utils.check_if_not_found(Track, method, track_name)
        if trackCheck != True:
            return trackCheck
        sessionCheck = api_utils.check_if_found(Session, method, session_name)
        if sessionCheck != True:
            return sessionCheck
        track = Track.objects.get(name=track_name)
        session = Session.objects.create(track_id=track.id, name=session_name)
        logger.info('%s: %s' % (method, session.name))
        result = ApiResult(method, ok=True, data=session)
        # TODO: Broadcast
        return result
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def change_session(session_name, new_session_name=None, new_track_name=None):
    '''Changes the session.'''
    '''Sends a broadcast message after session has been changed.'''
    # TODO: Role enforcement - admins only
    method = 'change_session'
    try:
        check = api_utils.check_if_not_found(Session, method, session_name)
        if check != True:
            return check
        if new_session_name == None and new_track_name == None:
            error = 'New session or track name is required' # TODO: i18n
            return ApiResult(method, ok=False, data=error)
        if new_session_name != None:
            check = api_utils.check_if_found(Session, method, new_session_name)
            if check != True:
                return check
        if new_track_name != None:
            check = api_utils.check_if_not_found(Track, method, new_track_name)
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
        result = ApiResult(method, ok=True, data=session)
        # TODO: Broadcast
        return result
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def remove_session(session_name):
    '''Removes a session, including all lap data.'''
    '''Sends a broadcast message after session has been removed.'''
    # TODO: Role enforcement - admins only
    method = 'remove_session'
    try:
        check = api_utils.check_if_not_found(Session, method, session_name)
        if check != True:
            return check
        session = Session.objects.get(name=session_name)
        session.delete()
        logger.info('%s: %s' % (method, session_name))
        result = ApiResult(method, ok=True, data=session_name)
        # TODO: Broadcast
        return result
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def get_session(session_name):
    '''Gets specified session.'''
    # TODO: Role enforcement - admins, riders or spectators
    method = 'get_session'
    try:
        check = api_utils.check_if_not_found(Session, method, session_name)
        if check != True:
            return check
        session = Session.objects.get(name=session_name)
        logger.info('%s: %s' % (method, session_name))
        return ApiResult(method, ok=True, data=session)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def get_sessions():
    '''Gets all sessions for all tracks.'''
    # TODO: Role enforcement - admins, riders or spectators
    method = 'get_sessions'
    try:
        sessions = Session.objects.all()
        logger.info('%s: %s' % (method, sessions))
        return ApiResult(method, ok=True, data=sessions)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def get_sessions_for_track(track_name):
    '''Gets all sessions for specified track.'''
    # TODO: Role enforcement - admins, riders or spectators
    method = 'get_sessions_for_track'
    try:
        check = api_utils.check_if_not_found(Track, method, track_name)
        if check != True:
            return check
        track = Track.objects.get(name=track_name)
        sessions = Session.objects.filter(track=track)
        logger.info('%s: %s' % (method, sessions))
        return ApiResult(method, ok=True, data=sessions)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def get_session_statistics(session_name):
    '''Gets all session statistics.'''
    # TODO: Role enforcement - admins, riders or spectators
    method = ''
    try:
        stats = 'TODO:'
        logger.info('%s: %s' % (method, stats))
        return ApiResult(method, ok=True, data=stats)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def get_session_lap_record(session_name):
    '''Gets statistics on session lap record.'''
    # TODO: Role enforcement - admins, riders or spectators
    method = ''
    try:
        stats = 'TODO:'
        logger.info('%s: %s' % (method, stats))
        return ApiResult(method, ok=True, data=stats)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def get_session_lap_average(session_name):
    '''Gets statistics on session lap average.'''
    # TODO: Role enforcement - admins, riders or spectators
    method = ''
    try:
        stats = 'TODO:'
        logger.info('%s: %s' % (method, stats))
        return ApiResult(method, ok=True, data=stats)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

