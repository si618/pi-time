from django.contrib import admin
from laptimer.models import Track, Rider, Session, Lap


admin.site.register(Track)
admin.site.register(Rider)
admin.site.register(Session)
admin.site.register(Lap)