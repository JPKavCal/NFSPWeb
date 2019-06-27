import os

from django.contrib.gis.utils import LayerMapping
from gaugedata.models import RiverGauge

gauge_mapping = {
    'dws_id': 'Station',
    'lat': 'Lat',
    'lon': 'Lon',
    'obsStart': 'Start_date',
    'obsEnd': 'End_date',
    'geom': 'POINT',
}

gauge_shp = os.path.abspath(os.path.join(os.getcwd(), 'shp_data', 'Stations.shp'))


def gauge_import(verbose=True):
    lm = LayerMapping(RiverGauge, gauge_shp, gauge_mapping, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)

if __name__ == '__main__':
    gauge_import()
