import django_settings
import datetime
from django.db import models
from django.conf import settings
from django.utils.timezone import localtime


class Track(models.Model):
	name = models.CharField(max_length=64, unique=True)
	distance = models.FloatField()
	timeout = models.PositiveSmallIntegerField()

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if (self.timeout is None):
			# Default to 2 seconds per metre/yard
			self.timeout = int(distance * 2)
		super(Track, self).save(*args, **kwargs)

class Session(models.Model):
	name = models.CharField(max_length=64, unique=True)
	track = models.ForeignKey(Track)
	start = models.DateTimeField()
	finish = models.DateTimeField(null=True, blank=True)

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if (self.start is None):
			self.start = datetime.datetime.now()
		super(Session, self).save(*args, **kwargs)

class Rider(models.Model):
	name = models.CharField(max_length=64, unique=True)

	def __unicode__(self):
		return self.name

class Lap(models.Model):
	session = models.ForeignKey(Session)
	rider = models.ForeignKey(Rider)
	start = models.DateTimeField()
	finish =  models.DateTimeField(null=True, blank=True)

	def __unicode__(self):
		if (self.finish is None):
			return 'Lap started ' + localtime(self.start).isoformat(' ')
		else:
			return 'Lap time ' + self.delta_to_str(self.finish - self.start)

	def save(self, *args, **kwargs):
		if (self.start is None):
			self.start = datetime.datetime.now()
		super(Lap, self).save(*args, **kwargs)

	def delta_to_str(self, delta):
		hours = delta.seconds // 3600
		minutes = (delta.seconds // 60) - (hours * 60)
		seconds = delta.seconds - minutes * 60 - hours * 3600
		milliseconds = delta.microseconds // 1000
		return '%s:%s:%s.%s' % (hours, minutes, seconds, milliseconds)

	def avg_speed_per_hour(self):
		if (self.finish is None):
			return None
	    # 3600 seconds in a hour / 1,000 metres in a kilometre
		avg_per_hour = self.avg_speed_per_second() * 3.6
		return avg_per_hour

	def avg_speed_per_second(self):
		if (self.finish is None):
			return None
		delta = self.finish - self.start
		avg_per_second = self.session.track.distance / delta.seconds
		return avg_per_second

class Settings(django_settings.db.Model):
	unit_of_measurement = models.CharField(max_length=2, choices=settings.UNIT_OF_MEASUREMENT, default=settings.METRIC)
	gpio_app = models.PositiveSmallIntegerField(default=11)
	gpio_sensor = models.PositiveSmallIntegerField(default=13)

	class Meta:
		abstract = True
		verbose_name_plural = 'Settings'

django_settings.register(Settings)
