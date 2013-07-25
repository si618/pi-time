import compute
import datetime
import django_settings
from django.conf import settings
from django.utils import timezone
from models import Track, Rider, Session, Lap


def get_all_data():
	'''Gets all track, session, rider, lap data and settings for backup.'''
	pass

# Rider functions

def add_rider(rider_name):
	'''Add a new rider. Rider name must be unique.'''
	pass

def change_rider(old_rider_name, new_rider_name):
	'''Changes the riders name. Rider name must be unique.'''
	pass

def remove_rider(rider_name):
	'''Removes a rider, including all track, session and lap data.'''
	pass

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


# Track related functions

def add_track(track_name, track_distance, lap_timeout_in_seconds):
	'''Add a new track. Track name must be unique.'''
	pass

def change_track(track_name, track_distance, lap_timeout_in_seconds):
	'''Changes the track details. Track name must be unique.'''
	pass

def remove_track(track_name):
	'''Removes a track, including all session and lap data.'''
	pass

def get_track_statistics(track_name):
	'''Gets all track statistics.'''

def get_track_lap_record(track_name):
	'''Gets statistics on track lap record.'''
	pass

def get_track_lap_average(track_name):
	'''Gets statistics on track lap average.'''
	pass


# Session functions

def start_session(track_name, session_name, started):
	'''Starts a new session. Session name must be unique.'''
	pass

def change_session_name(old_session_name, new_session_name):
	'''Changes the session name. Session name must be unique.'''
	pass

def change_session_track_name(session_name, old_track_name, new_track_name):
	'''Changes the session's track.'''
	pass

def change_session_start_time(session_name, old_start_time, new_start_time):
	'''Changes the session start time.'''
	pass

def change_session_end_time(session_name, old_end_time, new_end_time):
	'''Changes the session end time.'''
	pass

def end_session(session_name, end_time):
	'''Ends the session.'''
	pass

def remove_session(session_name):
	'''Removes a session, including all lap data.'''
	pass

def get_session_statistics(session_name):
	'''Gets all session statistics.'''

def get_session_lap_record(session_name):
	'''Gets statistics on session lap record.'''
	pass

def get_session_lap_average(session_name):
	'''Gets statistics on session lap average.'''
	pass


# Lap functions

def start_lap(session_name, rider_name, start_time):
	'''Starts a new lap.'''
	pass

def end_lap(session_name, rider_name, end_time):
	'''Ends the riders current lap.'''
	pass

def remove_lap(session_name, rider_name):
	'''Removes the riders current lap.'''
	pass
