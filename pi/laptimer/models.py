import django_settings
from django.db import models
from django.conf import settings


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
	end = models.DateTimeField(null=True, blank=True)

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
	end =  models.DateTimeField(null=True, blank=True)


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
	top = models.IntegerField()
'''
