from django.contrib.gis import admin
from .models import RiverGauge

# Register your models here.
admin.site.register(RiverGauge, admin.OSMGeoAdmin)
