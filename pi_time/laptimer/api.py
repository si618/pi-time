from autobahn.wamp1.protocol import exportRpc
from laptimer.models import ApiResult
import logging


logger = logging.getLogger('laptimer')

# General API functions

@exportRpc
def server_poweroff(reboot=False):
    '''Powers off the server after cancelling any unfinished laps.'''
    '''Invokes method: get_unfinished_laps and then cancel_lap.'''
    '''Sends a broadcast message to everyone before server is powered off.'''
    # TODO: Role enforcement - admins only
    method = 'server_poweroff'
    try:
        data = 'TODO: Shutting down server...'
        logger.info('%s: %s' % (method, data))
        # TODO: Broadcast to everyone
        # TODO: Shutdown/Reboot
        return ApiResult(method, ok=True, data=data)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)


@exportRpc
def backup_to_cloud(modified=None):
    '''If modified specified, only data on or after this time is backed up.'''
    '''Sends a broadcast message to admins once backup is complete.'''
    # TODO: Role enforcement - admins only
    method = 'backup_to_cloud'
    try:
        data='TODO: Cloud backup result...'
        logger.info('%s: %s' % (method, data))
        # TODO: Backup
        # TODO: Broadcast
        return ApiResult(method, ok=True, data=data)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)

@exportRpc
def get_all_data(modified=None):
    '''Gets track, session, rider, lap data and settings. Useful for backup.'''
    '''If modified is specified, only data on or after this time is returned.'''
    method = 'get_all_data'
    try:
        data='TODO: Data goes here...'
        logger.info('%s: %s' % (method, data))
        return ApiResult(method, ok=True, data=data)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)
