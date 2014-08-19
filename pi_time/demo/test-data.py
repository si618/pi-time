from django.conf import settings
from laptimer import api_lap, \
					 api_rider, \
					 api_session, \
					 api_track
					 #api_sensor, \
from laptimer.models import Lap, \
                            Rider, \
                            Session, \
                            Sensor, \
                            SensorEvent, \
                            Track
import logging


logger = logging.getLogger('laptimer')

# Create test data via api, assumes db is flushed
riderBetty = api_rider.add_rider(rider_name='Bodacious Betty').data
riderBob = api_rider.add_rider(rider_name='Bogus Bob').data
track = api_track.add_track(track_name='Test Track', track_distance=50, 
	lap_timeout=100, unit_of_measurement=settings.METRIC).data
session = api_session.add_session(track.name, 'Test Session').data
# sensorStart = api_sensor.add_sensor()
# sensorFinish = api_sensor.add_sensor()
# sensorStartFinish = api_sensor.add_sensor()
# riderBettyLap1 = api_lap.add_lap()
# riderBobLap1 = api_lap.add_lap()