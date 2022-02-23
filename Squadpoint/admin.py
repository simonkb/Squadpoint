from django.contrib import admin

# Register your models here.
from .models import User, Sport_court, Location, SportZone, Booking, Match, Notifications, Photo
admin.site.register(User)
admin.site.register(Sport_court)
admin.site.register(Location)
admin.site.register(SportZone)
admin.site.register(Booking)
admin.site.register(Match)
admin.site.register(Notifications)
admin.site.register(Photo)
