from laptimer.models import APIResult, Track, Rider, Session, Lap
import logging


logger = logging.getLogger(__name__)

class API:
	'''
	Application service layer, used by any client communicating with server.
	Client or sensor initiated data requests return an APIResult.	
	Server initiated broadcast messages return an APIBroadcast.
	'''
	def server_poweroff(self, reboot=False):
		'''Powers off the server after cancelling any unfinished laps.'''
		'''Invokes method: get_unfinished_laps and then cancel_lap.'''
		# TODO: Role enforcement - admins only
		pass

	def get_data(self, modified=None):
		'''
		Gets track, session, rider, lap data and settings. Useful for backup.
		If modified is specified, only data on or after this time is returned.
		'''
		return APIResult(result=True, data='Data goes here...')

	def get_unfinished_laps(self):
		'''Gets unfinished laps for all tracks.'''
		pass

	# Rider methods

	def add_rider(self, rider_name):
		'''Add a new rider. Rider name must be unique.'''
		'''Invokes method: broadcast_rider.'''
		return APIResult(result=True, data='Added rider: %s' % rider_name)

	def change_rider(self, rider_name, new_rider_name):
		'''Changes the riders name. Rider name must be unique.'''
		'''Invokes method: broadcast_rider.'''
		return APIResult(result=True, data='Changed rider from: %s to: %s'
			% (rider_name, new_rider_name))

	def remove_rider(self, rider_name):
		'''Removes a rider, including all track, session and lap data.'''
		'''Invokes method: broadcast_rider.'''
		# TODO: Role enforcement - admins only
		return APIResult(result=True, data='Removed rider %s: ' % rider_name)

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


	# Track related methods

	def add_track(self, track_name, track_distance, lap_timeout_in_seconds, 
		unit_of_measurement):
		'''Add a new track. Track name must be unique.'''
		'''Invokes method: broadcast_track.'''
		# TODO: Role enforcement - admins only
		pass

	def change_track(self, track_name, track_distance, lap_timeout_in_seconds,
		unit_of_measurement):
		'''Changes the track details. Track name must be unique.'''
		'''Invokes method: broadcast_track.'''
		# TODO: Role enforcement - admins only
		pass

	def remove_track(self, track_name):
		'''Removes a track, including all session and lap data.'''
		'''Invokes method: broadcast_track.'''
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


	# Session methods

	def start_session(self, track_name, session_name, started):
		'''Starts a new session. Session name must be unique.'''
		'''Invokes method: broadcast_session.'''
		# TODO: Role enforcement - admins only
		pass

	def change_session_name(self, old_session_name, new_session_name):
		'''Changes the session name. Session name must be unique.'''
		'''Invokes method: broadcast_session.'''
		# TODO: Role enforcement - admins only
		pass

	def change_session_track_name(self, session_name, old_track_name, new_track_name):
		'''Changes the session's track.'''
		'''Invokes method: broadcast_session.'''
		# TODO: Role enforcement - admins only
		pass

	def change_session_start_time(self, session_name, old_start_time, new_start_time):
		'''Changes the session start time.'''
		'''Invokes method: broadcast_session.'''
		# TODO: Role enforcement - admins only
		pass

	def change_session_end_time(self, session_name, old_end_time, new_end_time):
		'''Changes the session end time.'''
		'''Invokes method: broadcast_session.'''
		# TODO: Role enforcement - admins only
		pass

	def end_session(self, session_name, end_time):
		'''Ends the session.'''
		'''Invokes method: broadcast_session.'''
		# TODO: Role enforcement - admins only
		pass

	def remove_session(self, session_name):
		'''Removes a session, including all lap data.'''
		'''Invokes method: broadcast_session.'''
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
		'''Invokes method: broadcast_lap.'''
		pass

	def end_lap(self, session_name, rider_name, end_time):
		'''Ends the lap, and starts a new lap using the end time.'''
		'''Invokes method: broadcast_lap.'''
		pass

	def cancel_lap(self, session_name, rider_name, start_time):
		'''Cancels the current lap.'''
		'''Invokes method: broadcast_lap.'''
		pass

	def remove_lap(self, session_name, rider_name, start_time):
		'''Removes the lap. This is a soft delete and can be undone.'''
		'''Invokes method: broadcast_lap.'''
		# TODO: Role enforcement - admins only
		pass


	# Broadcast methods

	def broadcast_rider(self, rider):
		'''Send broadcast message that rider data was changed.'''
		pass

	def broadcast_track(self, track):
		'''Send broadcast message that track data was changed.'''
		pass

	def broadcast_session(self, session):
		'''Send broadcast message that session data was changed.'''
		pass

	def broadcast_lap(self, lap):
		'''Send broadcast message that lap data was changed.'''
		pass
