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
    '''
    Adds a new session. Session name must be unique for track.

    :param track_name: Name of track.
    :type track_name: str
    :param session_name: Name of session. Must exist for track.
    :type session_name: str

    :authorization: Administrators.
    :broadcast: Administrators, riders and spectators.
    :returns: Details of new session.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'add_session'
    try:
        check = api_utils.check_if_not_found(Track, method, track_name)
        if check != True:
            return check
        track = Track.objects.get(name=track_name)
        if Session.objects.filter(track=track, name=session_name).exists():
            error = 'Session already exists'
            return ApiResult(method, ok=False, data=error)
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
def change_session(track_name, session_name, new_session_name=None, 
    new_track_name=None):
    '''
    Changes the session or track name.

    :param track_name: Name of track.
    :type track_name: str
    :param session_name: Current session name. Must exist for track.
    :type session_name: str
    :param session_name: New unique session name.
    :type session_name: str

    :authorization: Administrators.
    :broadcast: Administrators, riders and spectators.
    :returns: Details of changed session.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''    
    method = 'change_session'
    try:
        check = api_utils.check_if_not_found(Track, method, track_name)
        if check != True:
            return check
        if not Session.objects.filter(track__name=track_name, 
            name=session_name).exists():
            error = 'Session not found'
            return ApiResult(method, ok=False, data=error)
        if new_session_name == None and new_track_name == None:
            error = 'New session or track name is required' # TODO: i18n
            return ApiResult(method, ok=False, data=error)
        if new_track_name != None:
            check = api_utils.check_if_not_found(Track, method, new_track_name)
            if check != True:
                return check
        session = Session.objects.get(name=session_name)
        if new_session_name != None:
            if Session.objects.filter(track=session.track, 
                name=new_session_name).exists():
                error = 'Session already exists'
                return ApiResult(method, ok=False, data=error)
            session.name = new_session_name
        if new_track_name != None:
            session.track = Track.objects.get(name=new_track_name)
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
def finish_session(track_name, session_name):
    '''
    Finishes a session.

    :param track_name: Name of track.
    :type track_name: str
    :param session_name: Name of session. Must exist for track.
    :type session_name: str

    :authorization: Administrators.
    :broadcast: Administrators, riders and spectators.
    :returns: Details of finished session.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'finish_session'
    try:
        check = api_utils.check_if_not_found(Track, method, track_name)
        if check != True:
            return check
        if not Session.objects.filter(track__name=track_name, 
            name=session_name).exists():
            error = 'Session not found'
            return ApiResult(method, ok=False, data=error)
        session = Session.objects.get(name=session_name, 
            track__name=track_name)
        session.finish = timezone.now()
        session.save()
        logger.info('%s: %s' % (method, session_name))
        result = ApiResult(method, ok=True, data=session_name)
        # TODO: Broadcast
        return result
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def remove_session(track_name, session_name):
    '''
    Removes a session, including all lap data.

    :param track_name: Name of track.
    :type track_name: str
    :param session_name: Name of session. Must exist for track.
    :type session_name: str

    :authorization: Administrators.
    :broadcast: Administrators, riders and spectators.
    :returns: Details of removed session.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'remove_session'
    try:
        check = api_utils.check_if_not_found(Track, method, track_name)
        if check != True:
            return check
        if not Session.objects.filter(name=session_name, 
            track__name=track_name).exists():
            error = 'Session not found'
            return ApiResult(method, ok=False, data=error)
        session = Session.objects.get(name=session_name, 
            track__name=track_name)
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
def get_sessions(track_name):
    '''
    Gets all sessions for a track.

    :param track_name: Name of track.
    :type track_name: str

    :authorization: Administrators, riders and spectators.
    :returns: Details of track sessions.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'get_sessions'
    try:
        check = api_utils.check_if_not_found(Track, method, track_name)
        if check != True:
            return check
        sessions = Session.objects.filter(track__name=track_name)
        logger.info('%s: %s' % (method, sessions))
        return ApiResult(method, ok=True, data=sessions)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def get_session_statistics(track_name, session_name):
    '''
    Gets session statistics for all riders.

    :param track_name: Name of track.
    :type track_name: str
    :param session_name: Name of session. Must exist for track.
    :type session_name: str

    :authorization: Administrators, riders and spectators.
    :returns: Session statistics.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'get_session_statistics'
    try:
        stats = 'TODO: Get session statistics'
        logger.info('%s: %s' % (method, stats))
        return ApiResult(method, ok=True, data=stats)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

