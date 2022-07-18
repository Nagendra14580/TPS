from django.contrib import admin
from TPS_app.models import Teams, TPS_Users, Locations, Schedules
from django.contrib.auth import get_user_model

user=get_user_model()
admin.site.register(user)

admin.site.register(Teams)
admin.site.register(Locations)
admin.site.register(Schedules)
# admin.site.register(User)

