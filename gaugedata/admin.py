from django.contrib.gis import admin
from .models import RiverGauge, Catchment

# Register your models here.
admin.site.register(RiverGauge, admin.OSMGeoAdmin)
admin.site.register(Catchment, admin.OSMGeoAdmin)
