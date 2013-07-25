import django_settings
from django.conf import settings

def average_kilometres_per_hour(start, finish, metres):
	avg_per_second = average_speed_per_second(start, finish, metres)
	if (avg_per_second is None):
		return None
	# Shortcut 3600 seconds in a hour / 1,000 metres in a kilometre
	avg_km_per_hour = avg_per_second * 3.6
	return round(avg_km_per_hour, 4)

def average_miles_per_hour(start, finish, yards):
	avg_per_second = average_speed_per_second(start, finish, yards)
	if (avg_per_second is None):
		return None
	avg_miles_per_hour = avg_per_second * 2.04545455
	return round(avg_miles_per_hour, 4)

def average_speed_per_hour(start, finish, distance):
	unit = django_settings.get('unit_of_measurement', default=settings.METRIC)
	if (unit == settings.METRIC):
		return average_kilometres_per_hour(start, finish, distance)
	else:
		return average_miles_per_hour(start, finish, distance)

def average_speed_per_second(start, finish, distance):
	if (start is None or finish is None):
		return None
	if (finish <= start):
		raise ValueError('Start time must be before finish time!')
	if (distance <= 0):
		raise ValueError('Track distance must be greater than zero!')
	delta = finish - start
	avg_per_second = float(distance) / delta.seconds
	return avg_per_second
