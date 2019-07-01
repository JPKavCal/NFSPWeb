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
    # return render(request, 'gaugedata/dfe.html')

    gauges = RiverGauge.objects.all()  # use filter() when you have sth to filter ;)
    form = request.POST  # you seem to misinterpret the use of form from django and POST data. you should take a look
                         # at [Django with forms][1]
    # you can remove the preview assignment (form =request.POST)
    # if request.method == 'POST':
        # selected_item = get_object_or_404(Item, pk=request.POST.get('item_id'))
        # get the user you want (connect for example) in the var "user"
        # user.item = selected_item
        # user.save()

        # Then, do a redirect for example

    return render_to_response('gaugedata/dfe.html', {'gauges': gauges})  #, context_instance=RequestContext(request), )