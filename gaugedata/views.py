from django.shortcuts import render, render_to_response
from .models import RiverGauge
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


# Create your views here.
@login_required
def gauges(request):
    return render(request, 'gaugedata/gauges.html')


@login_required
def dfe(request):
    gauges = RiverGauge.objects.all()

    return render_to_response('gaugedata/dfe.html', {'gauges': gauges, 'user': request.user})