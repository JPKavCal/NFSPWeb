import os

from django.contrib.gis.utils import LayerMapping
from gaugedata.models import RiverGauge, Catchment

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


catch_mapping = {
    'dws_id': 'gauge',
    'area': 'Area',
    'arf': 'ARF',
    'lc': 'Lc',
    's1085': 'S_1085',
    'tc': 'Tc',
    'dr2': 'DR2yr',
    'dr5': 'DR5yr',
    'dr10': 'DR10yr',
    'dr20': 'DR20yr',
    'dr50': 'DR50yr',
    'dr100': 'DR100yr',
    'dr200': 'DR200yr',
    'geom': 'POLYGON',
}

catch_shp = os.path.abspath(os.path.join(os.getcwd(), 'shp_data', 'WSPop_A.shp'))


def catch_import(verbose=True):
    lm = LayerMapping(Catchment, catch_shp, catch_mapping, transform=False, encoding='utf-8')
    lm.save(strict=True, verbose=verbose)


if __name__ == '__main__':
    # gauge_import()
    catch_import()
