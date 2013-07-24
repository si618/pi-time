import django_settings
from django.conf import settings

def avg_kilometres_per_hour(start, finish, distance):
	# 3600 seconds in a hour / 1,000 metres in a kilometre
	avg_per_second = avg_speed_per_second(start, finish, distance)
	if (avg_per_second is None):
		return None
	avg_km_per_hour = avg_per_second * 3.6
	return avg_km_per_hour

def avg_miles_per_hour(start, finish, distance):
	avg_km_per_hour = avg_kilometres_per_hour(start, finish, distance)
	if (avg_km_per_hour is None):
		return None
	avg_miles_per_hour = avg_km_per_hour * 0.621371192
	return avg_miles_per_hour

def avg_speed_per_hour(start, finish, distance):
	if (django_settings.exists('unit_of_measurement')):
		unit_of_measurement = django_settings.get('unit_of_measurement')
	else:
		unit_of_measurement = settings.METRIC
	if (unit_of_measurement == settings.METRIC):
		return avg_kilometres_per_hour(start, finish, distance)
	else:
		avg_miles_per_hour(start, finish, distance)

def avg_speed_per_second(start, finish, distance):
	if (start is None or finish is None):
		return None
	if (finish <= start):
		raise Exception('Start time must be before finish time!')
	if (float(distance) <= 0):
		raise Exception('Track distance must be greater than zero!')
	delta = finish - start
	avg_per_second = distance / delta.seconds
	return avg_per_second
