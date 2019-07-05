from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import RiverGauge, Catchment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models.functions import Substr


# Create your views here.
@login_required
def gauges(request):
    return render(request, 'gaugedata/gauges.html')


@login_required
def dfe(request):
    gauges = RiverGauge.objects.all()
    region = ['A', 'B', 'C', 'D', 'E', 'G', 'H', 'J', 'K', 'L', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']

    if request.method == 'POST':
        name = request.POST['station']
    else:
        name = None

    return render(request, 'gaugedata/dfe.html', {'gauges': gauges,
                                                  'user': request.user,
                                                  'name': name,
                                                  'regions': region})


@login_required
def gauge_data(request):
    if request.method == 'POST':
        try:
            gauge = RiverGauge.objects.get(pk=request.POST['station'])
            lat, lon = round(gauge.lat, 4), round(gauge.lon, 4)
        except ObjectDoesNotExist:
            lat, lon = 0, 0

        try:
            catch = Catchment.objects.get(pk=request.POST['station'])
            poly = [[round(x[1], 4), round(x[0], 4)] for x in catch.geom.coords[0][::3]]
        except ObjectDoesNotExist:
            poly = [[0, 0]]

        return JsonResponse({'lat': lat, 'lon': lon, 'poly': poly})


@login_required
def region_data(request):
    if request.method == 'POST':
        try:
            qs = RiverGauge.objects.annotate(fl_name=Substr('dws_id', 1, 1))
            qs = qs.filter(fl_name=request.POST['region'])
        except ObjectDoesNotExist:
            qs = []

        return render(request, 'gaugedata/gauge_dropdown.html', {'gauges': qs})
