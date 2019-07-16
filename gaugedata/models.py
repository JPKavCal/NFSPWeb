from django.contrib.gis.db import models
from django.db.models import Manager as GeoManager
from django.forms import ModelForm


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


class Catchment(models.Model):
    dws_id = models.CharField(primary_key=True, max_length=8)
    area = models.DecimalField(max_digits=15, decimal_places=4)
    arf = models.DecimalField(max_digits=15, decimal_places=1)
    lc = models.DecimalField(max_digits=15, decimal_places=0)
    s1085 = models.DecimalField(max_digits=15, decimal_places=4)
    tc = models.DecimalField(max_digits=15, decimal_places=2)
    dr2 = models.IntegerField()
    dr5 = models.IntegerField()
    dr10 = models.IntegerField()
    dr20 = models.IntegerField()
    dr50 = models.IntegerField()
    dr100 = models.IntegerField()
    dr200 = models.IntegerField()
    geom = models.PolygonField()
    objects = GeoManager()


class CatchForm(ModelForm):
    class Meta:
        model = Catchment
        exclude = ['dws_id', 'geom', 'dr2', 'dr5', 'dr10', 'dr20', 'dr50', 'dr100', 'dr200']
        labels = {
            "area": "Catchment Area (km\xB2)",
            "arf": "Aerial Reduction Factor (%)",
            "lc": "Length to Centroid (m)",
            "s1085": "Catchment Slope (m/m - 10-85)",
            "tc": "Time of Concentration (hours)",
            # "dr2": "Design Rainfall Depth (mm - 2yr)",
            # "dr5": "Design Rainfall Depth (mm - 5yr)",
            # "dr10": "Design Rainfall Depth (mm - 10yr)",
            # "dr20": "Design Rainfall Depth (mm - 20yr)",
            # "dr50": "Design Rainfall Depth (mm - 50yr)",
            # "dr100": "Design Rainfall Depth (mm - 100yr)",
            # "dr200": "Design Rainfall Depth (mm - 200yr)",

        }