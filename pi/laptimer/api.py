from django.db import transaction
from laptimer.models import APIResult, APIBroadcast, Track, Rider, Session, Lap
import logging


logger = logging.getLogger('laptimer')

class API:
    '''Interface for client communication with a lap timer server.'''

    def server_poweroff(self, reboot=False):
        '''Powers off the server after cancelling any unfinished laps.'''
        '''Invokes method: get_unfinished_laps and then cancel_lap.'''
        '''Sends a broadcast message before server is powered off.'''
        # TODO: Role enforcement - admins only
        pass

    def get_data(self, modified=None):
        '''
        Gets track, session, rider, lap data and settings. Useful for backup.
        If modified is specified, only data on or after this time is returned.
        '''
        return APIResult('get_data', result=True, data='Data goes here...')

    def get_unfinished_laps(self, track_name=None):
        '''Gets unfinished laps.'''
        pass

    # Rider methods

    def add_rider(self, rider_name):
        '''Add a new rider. Rider name must be unique.'''
        '''Sends a broadcast message after rider has been added.'''
        #check = self._check_if_rider_exists('add_rider', rider_name)
        #if check != True:
        #    return check
        try:
            rider = Rider.objects.create(name=rider_name)
            logger.info('Added rider: ' + rider.name)
            return APIResult('add_rider', result=True, data=rider)
        except Exception as e:
            logger.error('Exception caught in add_rider: %s' % e)
            return APIResult('add_rider', result=False, data=e)

    def change_rider(self, rider_name, new_rider_name):
        '''Changes the riders name. Rider name must be unique.'''
        '''Sends a broadcast message after rider has been changed.'''
        check = self._check_if_rider_exists('change_rider', new_rider_name)
        if check != True:
            return check
        check = self._check_if_rider_not_found('change_rider', rider_name)
        if check != True:
            return check
        rider = Rider.objects.get(name=rider_name)
        rider.name = new_rider_name
        rider.save()
        return APIResult('change_rider', result=True, data=rider)

    def remove_rider(self, rider_name):
        '''Removes a rider, including all track, session and lap data.'''
        '''Sends a broadcast message after rider has been removed.'''
        # TODO: Role enforcement - admins only
        check = self._check_if_rider_not_found('remove_rider', rider_name)
        if check != True:
            return check
        rider = Rider.objects.get(name=rider_name)
        rider.delete()
        return APIResult('remove_rider', result=True, data=rider_name)

    def get_rider_laps(self, rider_name):
        '''Gets statistics on a riders completed laps for all tracks.'''
        pass

    def get_rider_track_laps(self, rider_name, track_name):
        '''Gets statistics on a riders completed laps for a track.'''
        pass

    def get_rider_track_record(self, rider_name, track_name):
        '''Gets statistics on a riders lap record for a track.'''
        pass

    def get_rider_track_average(self, rider_name, track_name):
        '''Gets statistics on a riders lap average for a track.'''
        pass

    def get_rider_session_laps(self, rider_name, session_name):
        '''Gets statistics on a riders completed laps for a session.'''
        pass

    def get_rider_session_record(self, rider_name, session_name):
        '''Gets statistics on a riders lap record for a session.'''
        pass

    def get_rider_session_average(self, rider_name, session_name):
        '''Gets statistics on a riders lap average for a session.'''
        pass

    def get_rider_lap_current(self, rider_name, session_name):
        '''Gets statistics on a riders current lap.'''
        pass

    def get_rider_lap_previous(self, rider_name, session_name):
        '''Gets statistics on a riders previous lap.'''
        pass

    def _check_if_rider_exists(self, calling_method, rider_name):
        if Rider.objects.filter(name=rider_name).exists():
            error = 'Rider already exists' # TODO: i18n
            return APIResult(calling_method, result=False, data=error)
        return True

    def _check_if_rider_not_found(self, calling_method, rider_name):
        if not Rider.objects.filter(name=rider_name).exists():
            error = 'Rider not found' # TODO: i18n
            return APIResult(calling_method, result=False, data=error)
        return True

    # Track methods

    def add_track(self, track_name, track_distance, lap_timeout,
        unit_of_measurement):
        '''Add a new track. Track name must be unique.'''
        '''Sends a broadcast message after track has been added.'''
        # TODO: Role enforcement - admins only
        check = self._check_if_track_exists('add_track', track_name)
        if check != True:
            return check
        track = Track.objects.create(name=track_name, distance=track_distance,
            timeout=lap_timeout, unit_of_measurement=unit_of_measurement)
        return APIResult('add_track', result=True, data=track)

    def change_track(self, track_name, track_distance, lap_timeout,
        unit_of_measurement):
        '''Changes the track details. Track name must be unique.'''
        '''Sends a broadcast message after track has been changed.'''
        # TODO: Role enforcement - admins only
        pass

    def remove_track(self, track_name):
        '''Removes a track, including all session and lap data.'''
        '''Sends a broadcast message after track has been removed.'''
        # TODO: Role enforcement - admins only
        pass

    def get_track_statistics(self, track_name):
        '''Gets all track statistics.'''
        pass

    def get_track_lap_record(self, track_name):
        '''Gets statistics on track lap record.'''
        pass

    def get_track_lap_average(self, track_name):
        '''Gets statistics on track lap average.'''
        pass

    def _check_if_track_exists(self, calling_method, track_name):
        if Track.objects.filter(name=track_name).exists():
            error = 'Track already exists' # TODO: i18n
            return APIResult(calling_method, result=False, data=error)
        return True

    def _check_if_track_not_found(self, calling_method, track_name):
        if not Track.objects.filter(name=track_name).exists():
            error = 'Track not found' # TODO: i18n
            return APIResult(calling_method, result=False, data=error)
        return True


    # Session methods

    def add_session(self, track_name, session_name):
        '''Adds a new session. Session name must be unique.'''
        '''Sends a broadcast message after session has been added.'''
        # TODO: Role enforcement - admins only
        pass

    def change_session(self, session_name, new_session_name=None,
        new_track_name=None, new_start_time=None, new_end_time=None):
        '''Changes the session.'''
        '''Sends a broadcast message after session has been changed.'''
        # TODO: Role enforcement - admins only
        pass

    def remove_session(self, session_name):
        '''Removes a session, including all lap data.'''
        '''Sends a broadcast message after session has been removed.'''
        # TODO: Role enforcement - admins only
        pass

    def start_session(self, session_name, started):
        '''Starts a session.'''
        '''Sends a broadcast message after session has started.'''
        # TODO: Role enforcement - admins only
        pass

    def end_session(self, session_name, end_time):
        '''Ends the session.'''
        '''Sends a broadcast message after session has ended.'''
        # TODO: Role enforcement - admins only
        pass

    def get_session_statistics(self, session_name):
        '''Gets all session statistics.'''

    def get_session_lap_record(self, session_name):
        '''Gets statistics on session lap record.'''
        pass

    def get_session_lap_average(self, session_name):
        '''Gets statistics on session lap average.'''
        pass


    # Lap methods

    def start_lap(self, session_name, rider_name, start_time):
        '''Starts a new lap.'''
        '''Sends a broadcast message after lap has started.'''
        # TODO: Role enforcement - sensor only
        pass

    def end_lap(self, session_name, rider_name, end_time):
        '''
        Ends the lap, starting a new lap using the end time as new start time.
        Sends a broadcast message after lap has ended.
        '''
        # TODO: Role enforcement - sensor only
        pass

    def cancel_lap(self, session_name, rider_name, start_time):
        '''Cancels the current lap.'''
        '''Sends a broadcast message after lap has been cancelled.'''
        # TODO: Role enforcement - only admin or current rider
        pass

    def remove_lap(self, session_name, rider_name, start_time):
        '''Removes the lap. This is a soft delete and can be undone.'''
        '''Sends a broadcast message after lap has been removed.'''
        # TODO: Role enforcement - admins only
        pass
