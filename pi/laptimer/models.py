from django.db import models

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

"""
class Settings(models.Model):
	METRIC = 'SI'
	IMPERIAL = 'IMP'
	UNIT_OF_MEASUREMENT = (
		(METRIC, 'Metric'),
		(IMPERIAL, 'Imperial'),
	)
	unit_of_measurement = models.CharField(max_length=3, choices=UNIT_OF_MEASUREMENT, default=METRIC)

	class Meta:
		verbose_name_plural = 'Settings'

class QueryCriteria(models.Model):
	track = models.ForeignKey(Track)
	session = models.ForeignKey(Session)
	rider = models.ForeignKey(Rider)
	top = models.IntegerField()
"""
