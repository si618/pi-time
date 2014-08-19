from django.contrib import admin
from laptimer.models import Lap, \
							Rider, \
							Session, \
							Sensor, \
							SensorEvent, \
							Track

admin.site.register(Lap)
admin.site.register(Rider)
admin.site.register(Session)
admin.site.register(Sensor)
admin.site.register(SensorEvent)
admin.site.register(Track)
