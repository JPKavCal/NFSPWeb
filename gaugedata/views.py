from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import RiverGauge, Catchment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Create your views here.
@login_required
def gauges(request):
    return render(request, 'gaugedata/gauges.html')


@login_required
def dfe(request):
    gauges = RiverGauge.objects.all()

    if request.method == 'POST':
        name = request.POST['station']
    else:
        name = None

    return render(request, 'gaugedata/dfe.html', {'gauges': gauges, 'user': request.user, 'name': name})


@login_required
def gauge_data(request):
    if request.method == 'POST':
        try:
            gauge = RiverGauge.objects.get(pk=request.POST['station'])
            lat, lon = gauge.lat, gauge.lon
            catch = Catchment.objects.get(pk=request.POST['station'])
            poly = catch.geom.coords[0]
        except ObjectDoesNotExist:
            lat, lon = 0, 0
            poly = [[0, 0]]
        return JsonResponse({'lat': round(lat, 3), 'lon': round(lon, 3), 'poly': poly})
