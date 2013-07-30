from django.conf import settings
from django.utils import timezone
from laptimer.models import APIResult, Track, Rider, Session, Lap
import compute
import datetime
import django_settings
import logging


logger = logging.getLogger(__name__)

class API:
	'''Application service layer. All methods must return APIResult.'''

	def get_all_data(self):
		'''Gets all track, session, rider, lap data and settings.'''
		return APIResult(result=True, data='Track data goes here...')

	# Rider functions

	def add_rider(self, rider_name):
		'''Add a new rider. Rider name must be unique.'''
		return APIResult(result=True, data='Added rider: %s' % rider_name)

	def change_rider(self, rider_name, new_rider_name):
		'''Changes the riders name. Rider name must be unique.'''
		return APIResult(result=True, data='Changed rider from: %s to: %s'
			% (rider_name, new_rider_name))

	def remove_rider(self, rider_name):
		'''Removes a rider, including all track, session and lap data.'''
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


	# Track related functions

	def add_track(self, track_name, track_distance, lap_timeout_in_seconds, 
		unit_of_measurement):
		'''Add a new track. Track name must be unique.'''
		pass

	def change_track(self, track_name, track_distance, lap_timeout_in_seconds,
		unit_of_measurement):
		'''Changes the track details. Track name must be unique.'''
		pass

	def remove_track(self, track_name):
		'''Removes a track, including all session and lap data.'''
		pass

	def get_track_statistics(self, track_name):
		'''Gets all track statistics.'''

	def get_track_lap_record(self, track_name):
		'''Gets statistics on track lap record.'''
		pass

	def get_track_lap_average(self, track_name):
		'''Gets statistics on track lap average.'''
		pass


	# Session functions

	def start_session(self, track_name, session_name, started):
		'''Starts a new session. Session name must be unique.'''
		pass

	def change_session_name(self, old_session_name, new_session_name):
		'''Changes the session name. Session name must be unique.'''
		pass

	def change_session_track_name(self, session_name, old_track_name, new_track_name):
		'''Changes the session's track.'''
		pass

	def change_session_start_time(self, session_name, old_start_time, new_start_time):
		'''Changes the session start time.'''
		pass

	def change_session_end_time(self, session_name, old_end_time, new_end_time):
		'''Changes the session end time.'''
		pass

	def end_session(self, session_name, end_time):
		'''Ends the session.'''
		pass

	def remove_session(self, session_name):
		'''Removes a session, including all lap data.'''
		pass

	def get_session_statistics(self, session_name):
		'''Gets all session statistics.'''

	def get_session_lap_record(self, session_name):
		'''Gets statistics on session lap record.'''
		pass

	def get_session_lap_average(self, session_name):
		'''Gets statistics on session lap average.'''
		pass


	# Lap functions

	def start_lap(self, session_name, rider_name, start_time):
		'''Starts a new lap.'''
		pass

	def end_lap(self, session_name, rider_name, end_time):
		'''Ends the lap.'''
		pass

	def remove_lap(self, session_name, rider_name, start_time):
		'''Removes the lap.'''
		pass
