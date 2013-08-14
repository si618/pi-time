from django.conf import settings
from django.db import models
from django.utils import timezone
import django_settings
import json
import utils


# API models

class APIBase:

    class Meta:
        abstract = True

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

class APIResult(APIBase):
    call = str
    result = bool
    data = object

    def __init__(self, call, result=False, data=None):
        self.call = call
        self.result = result
        self.data = data

class APIBroadcast(APIBase):
    event = str
    data = object

    def __init__(self, event, data=None):
        self.event = event
        self.data = data


# Setting models

class Boolean(django_settings.db.Model):
    value = models.BooleanField()

    class Meta:
        abstract = True

class GPIOLayout(django_settings.db.Model):
    value = models.PositiveSmallIntegerField(max_length=2,
        choices=settings.GPIO_LAYOUT)

    class Meta:
        abstract = True

class UnitOfMeasurement(django_settings.db.Model):
    value = models.CharField(max_length=2,
        choices=settings.UNIT_OF_MEASUREMENT)

    class Meta:
        abstract = True

django_settings.register(Boolean)
django_settings.register(GPIOLayout)
django_settings.register(UnitOfMeasurement)


# Django Data models

class CommonBase(models.Model):
    modified = models.DateTimeField(default=timezone.now())

    class Meta:
        abstract = True

class Track(CommonBase):
    name = models.CharField(max_length=64, unique=True)
    distance = models.FloatField()
    timeout = models.PositiveSmallIntegerField()
    unit_of_measurement = models.CharField(max_length=2,
        choices=settings.UNIT_OF_MEASUREMENT, default=settings.METRIC)

    def save(self, *args, **kwargs):
        if (self.timeout is None):
            self.timeout = int(self.distance * 2)
        super(Track, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class Session(CommonBase):
    name = models.CharField(max_length=64, unique=True)
    track = models.ForeignKey(Track)
    start = models.DateTimeField()
    finish = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if (self.start is None):
            self.start = timezone.now()
        super(Session, self).save(*args, **kwargs)

class Rider(CommonBase):
    name = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.name

class Lap(CommonBase):
    session = models.ForeignKey(Session)
    rider = models.ForeignKey(Rider)
    start = models.DateTimeField()
    finish =  models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        if (self.finish is None):
            elapsed = timezone.now()
            return utils.time_to_str(self.start, elapsed) + ' (Incomplete)'
        else:
            return utils.time_to_str(self.start, self.finish)

    def save(self, *args, **kwargs):
        if (self.start is None):
            self.start = timezone.now()
        if (self.finish is not None and self.finish <= self.start):
            raise ValueError('Start time must be before finish time!')
        super(Lap, self).save(*args, **kwargs)

    def lap_time_in_seconds(self):
        if (self.finish is None):
            finish = timezone.now()
        else:
            finish = self.finish
        delta = finish - self.start
        return delta.total_seconds()

    def average_speed_per_hour(self):
        return compute.average_speed_per_hour(self.start, self.finish,
            self.session.track.distance)

    def average_speed_per_second(self):
        return compute.average_speed_per_second(self.start, self.finish,
            self.session.track.distance)

class RecordBase(CommonBase):
    rider = models.ForeignKey(Rider)
    lap = models.ForeignKey(Lap)

    class Meta:
        abstract = True

    def __unicode__(self):
        return '%s\n%s\n%s\n%s' % (track, session, rider, lap)

class CurrentTrackRecord(CommonBase):
    pass

class CurrentSessionRecord(CommonBase):
    pass

class CurrentRiderTrackRecord(CommonBase):
    pass

class CurrentRiderSessionRecord(CommonBase):
    pass
