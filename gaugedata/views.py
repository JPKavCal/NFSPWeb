from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def gauges(request):
    return render(request, 'gaugedata/gauges.html')


@login_required
def dfe(request):
    return render(request, 'gaugedata/dfe.html')