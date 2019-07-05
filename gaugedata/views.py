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
        except ObjectDoesNotExist:
            lat, lon = 0, 0

        try:
            catch = Catchment.objects.get(pk=request.POST['station'])
            poly = [[round(x[1],4), round(x[0],4)] for x in catch.geom.coords[0]]
        except ObjectDoesNotExist:
            poly = [[0, 0]]

        return JsonResponse({'lat': round(lat, 3), 'lon': round(lon, 3), 'poly': poly})
