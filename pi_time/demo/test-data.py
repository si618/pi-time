from django.conf import settings
from laptimer import api
from laptimer.models import Lap, \
                            Rider, \
                            Session, \
                            Sensor, \
                            SensorEvent, \
                            Track
import logging


logger = logging.getLogger('laptimer')


# Create test data via api, assumes db is flushed
betty = api.add_rider(rider_name='Bodacious Betty').data
bob = api.add_rider(rider_name='Bogus Bob').data
track = api.add_track(track_name='Test Track', track_distance=50, 
	lap_timeout=100, unit_of_measurement=settings.METRIC)
session = api.add_session(track, 'Test Session').data
