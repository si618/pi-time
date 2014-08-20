from django.conf import settings
from django.db import models
from django.utils import timezone
from laptimer import utils
import copy
import django_settings
import jsonpickle
import logging


logger = logging.getLogger('laptimer')

# API models

class ApiBase:
    '''Abstract base class for API classes.'''   

    data = object
    '''Contains the payload data.'''   

    class Meta:
        abstract = True

    def toJSON(self):
        '''Converts object to Javascript Object Notation.'''
        clone = copy.deepcopy(self)
        if getattr(clone.data, '_state', False):
            del clone.data._state
        return jsonpickle.encode(clone, unpicklable=False)


class ApiResult(ApiBase):
    '''Represents the result from an API call.'''   
    
    call = str
    '''Name of API method called.'''   

    ok = bool
    '''Whether the API call was successful.'''   

    def __init__(self, call, ok=False, data=None):
        self.call = call
        self.ok = ok
        self.data = data


class ApiBroadcast(ApiBase):
    '''Represents an API broadcast.'''

    event = str
    '''Records the broadcast event.'''

    def __init__(self, event, data=None):
        self.event = event
        self.data = data


# Setting models

class Boolean(django_settings.db.Model):
    value = models.BooleanField(default=False)

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


# Django data models (users/groups/roles already handled by Django)

class CommonBase(models.Model):
    '''Abstract base class for Django data models.'''

    modified = models.DateTimeField()
    '''Records when model object was last modified.'''

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        '''Sets the modified property to the current time.'''
        self.modified = timezone.now()
        super(CommonBase, self).save(*args, **kwargs)


class Track(CommonBase):
    '''Defines the characteristics of a track.'''

    name = models.CharField(max_length=64, unique=True, db_index=True)
    '''Unique name of the track.'''

    distance = models.FloatField()
    '''Total distance of the track.'''

    timeout = models.PositiveSmallIntegerField()
    '''Number of seconds a lap time has elapsed before timing out.'''

    unit_of_measurement = models.CharField(max_length=2,
        choices=settings.UNIT_OF_MEASUREMENT, default=settings.METRIC)
    '''Unit of measurement used to define the track distance.'''

    def save(self, *args, **kwargs):
        '''Saves a track, timeout set to twice distance if not entered.'''
        if (self.timeout is None):
            self.timeout = int(self.distance * 2)
        super(Track, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Sensor(CommonBase):
    '''Defines the characteristics of a timing sensor.'''

    name = models.CharField(max_length=64, db_index=True)
    '''Name of the sensor. Must be unique for track.'''

    track = models.ForeignKey(Track)
    '''Track associated with sensor.'''

    sensor_type = models.CharField(max_length=2,
        choices=settings.SENSOR_TYPE, default=settings.SENSOR_TYPE_RPI)
    '''Type of sensor.'''

    sensor_pos = models.CharField(max_length=2,
        choices=settings.SENSOR_POS, default=settings.SENSOR_POS_START_FINISH)
    '''Position of sensor on track.'''

    # TODO: Optional foreign keys for previous/next TrackSector.

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'track')


class SensorEvent(CommonBase):
    '''Defines when a sensor event occurs during a lap.'''

    lap = models.ForeignKey('Lap')
    sensor = models.ForeignKey(Sensor)
    time = models.DateTimeField()

    def __unicode__(self):
        return '%s %s' % (self.sensor.name, timezone.localtime(self.time))


class Session(CommonBase):
    '''Defines a track session, or a group of laps over a period of time.'''

    name = models.CharField(max_length=64, db_index=True)
    '''Name of the session. Must be unique for track.'''

    track = models.ForeignKey(Track)
    '''Track associated with session.'''

    start = models.DateTimeField()
    '''Start time of session.'''

    finish = models.DateTimeField(null=True, blank=True)
    '''Finishing time of session.'''

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        '''Saves a session, start defaults to now if not entered.'''
        if (self.start is None):
            self.start = timezone.now()
        super(Session, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('name', 'track')


class Rider(CommonBase):
    '''Defines the characteristics of a rider.'''

    name = models.CharField(max_length=64, unique=True, db_index=True)
    '''Unique name of the rider.'''

    def __unicode__(self):
        return self.name


class Lap(CommonBase):
    session = models.ForeignKey(Session)
    rider = models.ForeignKey(Rider)
    start = models.ForeignKey(SensorEvent, related_name='lap_start', null=True, blank=True)
    finish = models.ForeignKey(SensorEvent, related_name='lap_finish', null=True, blank=True)

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
            finish = self.finish.time
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
    sensor_event = models.ForeignKey(SensorEvent)
'''
