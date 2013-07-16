from django.contrib import admin
#from laptimer.models import Settings
from laptimer.models import Track
from laptimer.models import Rider
from laptimer.models import Session
from laptimer.models import Lap

#admin.site.register(Settings)
admin.site.register(Track)
admin.site.register(Rider)
admin.site.register(Session)
admin.site.register(Lap)