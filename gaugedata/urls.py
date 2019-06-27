from django.conf.urls import url
from .views import gauges
from django.views.decorators.csrf import csrf_exempt

# SET THE NAMESPACE!
app_name = 'gaugedata'


urlpatterns=[
    url('map/', csrf_exempt(gauges), name='gauges'),
]
