# API for interacting with models.

#from laptimer import Rider
#from laptimer import Track
#from laptimer import Session
#from laptimer import Lap
#from laptimer import Setting


# Rider related functions

def rider_add(name):
	pass

def rider_change(old_name, new_name):
	pass

def rider_remove(name):
	pass


# Track related functions

def track_add(name, distance, timeout):
	pass

def track_change(name, distance, timeout):
	pass

def track_remove(name):
	pass


# Session related functions

def session_start(track, name):
	pass

def session_finish(name):
	pass

def session_remove(name):
	pass


# Lap related functions

def lap_start(session, rider, time):
	pass

def lap_finish(session, time):
	pass

def lap_timeout(session):
	pass


# Report related functions

def get_fastest_lap_time(track, session, rider):
	pass

def get_average_lap_time(track, session, rider):
	pass

def get_lap_count(track, session, rider):
	pass

def get_distance_ridden(track, session, rider):
	pass
