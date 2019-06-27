"""NFSPWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from gaugedata.models import RiverGauge
from rest_framework import routers, serializers, viewsets
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')


class RiverGaugeSerializer(GeoFeatureModelSerializer):
    # renderer_class = JSONRenderer

    # geom = GeometrySerializerMethodField()
    #
    # def get_geom(self, obj):
    #     return Point(obj.geom.coords[1], obj.geom.coords[0])

    class Meta:
        model = RiverGauge
        geo_field = 'geom'
        id_field = False
        fields = ('dws_id', 'obsStart', 'obsEnd')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RiverGaugeViewSet(viewsets.ModelViewSet):
    queryset = RiverGauge.objects.all()
    serializer_class = RiverGaugeSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'gauges', RiverGaugeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('gebruikers.urls', namespace='gebruik')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include((router.urls, 'api_app'), namespace='api')),
    path('K52748/', include('gaugedata.urls', namespace='K52748')),
    path('', include('NFSP_Website.urls', namespace='NFSP_Website')),
]
