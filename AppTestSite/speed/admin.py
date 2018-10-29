from django.contrib import admin

from .models import AppInformation, SpeedInformation

admin.site.register(AppInformation)
admin.site.register(SpeedInformation)
