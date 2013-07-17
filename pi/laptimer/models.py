import django_settings
from django.db import models
from django.conf import settings
from django.utils.timezone import localtime


class Track(models.Model):
	name = models.CharField(max_length=64, unique=True)
	distance = models.IntegerField(default=50)
	timeout = models.IntegerField(default=100)

	def __unicode__(self):
		return self.name    

class Session(models.Model):
	name = models.CharField(max_length=64, unique=True)
	track = models.ForeignKey(Track)
	start = models.DateTimeField()
	finish = models.DateTimeField(null=True, blank=True)

	def __unicode__(self):
		return self.name

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
			delta = self.finish - self.start
			minutes = delta.seconds // 60
			hours = delta.seconds // 3600
			minutes -= hours * 60
			seconds = delta.seconds - minutes * 60 - hours * 3600
			milliseconds = delta.microseconds // 1000			
			return 'Lap time ' + '%s:%s:%s.%s' % (hours, minutes, seconds, milliseconds)

class Settings(django_settings.db.Model):
	unit_of_measurement = models.CharField(max_length=2, choices=settings.UNIT_OF_MEASUREMENT, default=settings.METRIC)
	
	class Meta:
		abstract = True
		verbose_name_plural = 'Settings'

django_settings.register(Settings)

'''
class QueryCriteria(models.Model):
	track = models.ForeignKey(Track)
	session = models.ForeignKey(Session)
	rider = models.ForeignKey(Rider)
	top = IntegerField()
'''
