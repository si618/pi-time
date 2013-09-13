from django.conf import settings
from django.db import models
from django.utils import timezone
import copy
import django_settings
import jsonpickle
import logging
import utils


logger = logging.getLogger('laptimer')


# API models

class APIBase:
    data = object

    class Meta:
        abstract = True

    def toJSON(self):
        clone = copy.deepcopy(self)
        if getattr(clone.data, '_state', False):
            del clone.data._state
        return jsonpickle.encode(clone, unpicklable=False)


class APIResult(APIBase):
    call = str
    successful = bool

    def __init__(self, call, successful=False, data=None):
        self.call = call
        self.successful = successful
        self.data = data


class APIBroadcast(APIBase):
    event = str

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
        choices=settings.RPI_GPIO_LAYOUT)

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
    name = models.CharField(max_length=64, unique=True, db_index=True)
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


class Sensor(CommonBase):
    name = models.CharField(max_length=64, unique=True, db_index=True)
    track = models.ForeignKey(Track)
    sensor_type = models.CharField(max_length=2,
        choices=settings.SENSOR, default=settings.SENSOR_START_FINISH)
    # TODO: Optional foreign keys for previous/next TrackSector.

    def __unicode__(self):
        return self.name


class Session(CommonBase):
    name = models.CharField(max_length=64, unique=True, db_index=True)
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
    name = models.CharField(max_length=64, unique=True, db_index=True)

    def __unicode__(self):
        return self.name


class LapTime(CommonBase):
    lap = models.ForeignKey('Lap')
    sensor = models.ForeignKey(Sensor)
    time = models.DateTimeField()

    def __unicode__(self):
        return '%s %s' % (self.sensor.name, timezone.localtime(self.time))

class Lap(CommonBase):
    session = models.ForeignKey(Session)
    rider = models.ForeignKey(Rider)
    start = models.ForeignKey(LapTime, related_name='lap_start', null=True, blank=True)
    finish = models.ForeignKey(LapTime, related_name='lap_finish', null=True, blank=True)

    def __unicode__(self):
        if (self.finish.time is None):
            elapsed = timezone.now()
            return utils.time_to_string(self.start.time, elapsed) + ' (Incomplete)'
        else:
            return utils.time_to_string(self.start.time, self.finish.time)

    def save(self, *args, **kwargs):
        if (self.finish is not None and self.finish.time <= self.start.time):
            raise ValueError('Start time must be before finish time!')
        super(Lap, self).save(*args, **kwargs)

    def lap_time_in_seconds(self):
        if (self.finish.time is None):
            finish = timezone.now()
        else:
            finish = self.finish
        delta = finish - self.start.time
        return delta.total_seconds()

    def average_speed_per_hour(self):
        return compute.average_speed_per_hour(self.start.time, self.finish.time,
            self.session.track.distance)

    def average_speed_per_second(self):
        return compute.average_speed_per_second(self.start.time, self.finish.time,
            self.session.track.distance)

'''
TODO: Implement if/when sector times are wanted
class TrackSector(CommonBase):
    track = models.ForeignKey(Track)
    sensor = models.ForeignKey(Sensor)
    position = models.PositiveSmallIntegerField()
    distance = models.FloatField()

class LapSector(CommonBase):
    lap_time = models.ForeignKey(LapTime)
'''
