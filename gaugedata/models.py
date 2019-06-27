from django.contrib.gis.db import models
from django.db.models import Manager as GeoManager


# Create your models here.
class RiverGauge(models.Model):

    dws_id = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=25)
    lat = models.FloatField()
    lon = models.FloatField()
    obsStart = models.DateField()
    obsEnd = models.DateField()
    geom = models.PointField()
    objects = GeoManager()

    def __unicode__(self):
        return self.dws_id, self.name, self.obsStart, self.obsEnd
