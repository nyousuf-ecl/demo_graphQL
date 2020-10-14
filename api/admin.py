from django.contrib import admin

from api.models import Account, Location, Event, Event_member


admin.site.register(Account)
admin.site.register(Location)
admin.site.register(Event)
admin.site.register(Event_member)
