from django.conf.urls import url
from .views import gauges, dfe, gauge_data, region_data, catchform, stats_data

# SET THE NAMESPACE!
app_name = 'gaugedata'


urlpatterns=[
    url('map/', gauges, name='gauges'),
    url('dfe/', dfe, name='dfe'),
    url('gauged/', gauge_data, name='gauged'),
    url('regions/', region_data, name='regions'),
    url('catchform/', catchform, name='catchform'),
    url('statsdata/', stats_data, name='statsdata'),
]
