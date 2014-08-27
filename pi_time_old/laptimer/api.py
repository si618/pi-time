from autobahn.wamp1.protocol import exportRpc
from laptimer.models import ApiResult
import logging


logger = logging.getLogger('laptimer')

# General API functions

@exportRpc
def server_poweroff(cancel_unfinished_laps, reboot):
    '''
    Powers off the server.

    :param cancel_unfinished_laps: Cancel any unfinished laps before shutdown.
    :type cancel_unfinished_laps: Boolean
    :param reboot: Denoting whether server should be rebooted after shutdown.
    :type reboot: Boolean

    :authorization: Administrators.
    :broadcast: Administrators, riders, spectators and sensors.
    :returns: Details of impending shutdown.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
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
    '''
    Backup data to cloud.

    :param modified: Only data modified on or after this time is backed up.
    :type modified: datetime

    :authorization: Administrators.
    :broadcast: Administrators.
    :returns: Details of backup result.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
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
    '''
    Gets all data and settings.

    :param modified: Only data modified on or after this time is returned.
    :type modified: datetime

    :authorization: Administrators.
    :returns: Relevant data.
    :rtype: Instance of :class:`laptimer.models.ApiResult`.
    '''
    method = 'get_all_data'
    try:
        data='TODO: Data goes here...'
        logger.info('%s: %s' % (method, data))
        return ApiResult(method, ok=True, data=data)
    except Exception as e:
        logger.error('Exception caught in %s: %s' % (method, e))
        error = type(e).__name__
        return ApiResult(method, ok=False, data=error)
