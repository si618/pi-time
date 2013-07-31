
def time_to_string(start, finish):
	if (start is None or finish is None):
		return None
	if (finish <= start):
		raise ValueError('Start time must be before finish time!')
	delta = finish - start
	hours = delta.seconds // 3600
	minutes = (delta.seconds // 60) - (hours * 60)
	seconds = delta.seconds - minutes * 60 - hours * 3600
	milliseconds = delta.microseconds // 1000
	time = '%s:%s:%s.%s' % (hours, minutes, seconds, milliseconds)
	return time

