from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import RiverGauge, Catchment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models.functions import Substr
from bokeh.layouts import column, Spacer, row
from bokeh.plotting import figure
from bokeh.models import Range1d
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import CustomJS, ColumnDataSource, Slider


# Create your views here.
@login_required
def gauges(request):
    return render(request, 'gaugedata/gauges.html')


@login_required
def dfe(request):
    gauges = RiverGauge.objects.all()
    region = ['A', 'B', 'C', 'D', 'E', 'G', 'H', 'J', 'K', 'L', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']
    x = [1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995]
    y = [3, 4, 12, 1, 5, 13, 25, 12, 6, 7]

    TOOLTIPS = [
        ("Year", "@x"),
        ("Flow", "@y")
    ]

    if request.method == 'POST':
        name = request.POST['station']
    else:
        name = None

    source = ColumnDataSource(data=dict(x=x, y=y))

    # callback = CustomJS(args=dict(source=source), code="""
    #         var data = source.data;
    #         var f = cb_obj.value
    #         var x = data['x']
    #         var y = data['y']
    #         for (var i = 0; i < x.length + 3; i++) {
    #             y[i] = y[i] + f / 10
    #             x[i] = x[i] + f / 20
    #         }
    #         source.change.emit();
    #     """)

    # slider = Slider(start=0.1, end=4, value=1, step=.1, title="power")
    # slider.js_on_change('value', callback)

    plot = figure(
        sizing_mode='stretch_width',
        tools=['pan', 'box_zoom', 'save',
               'reset', 'wheel_zoom'],
        y_range=Range1d(min(y) * 0.8, max(y) * 1.1, bounds=(min(y) * 0.5, max(y) * 1.15)),
        x_range=Range1d(min(x), max(x), bounds=(min(x), max(x))),
        x_axis_label="Year",
        y_axis_label="Peak Flow (m³.s⁻¹)",
        # plot_width=450,
        plot_height=400,
        id='stat_fig',
        tooltips=TOOLTIPS
    )
    plot.line('x', 'y', source=source)
    plot.toolbar.logo = None
    t = Spacer()
    layout = row(plot, t)  # , slider

    script, div = components(layout, CDN)

    return render(request, 'gaugedata/dfe.html', {'gauges': gauges,
                                                  'user': request.user,
                                                  'name': name,
                                                  'regions': region,
                                                  "bokeh_script": script,
                                                  "bokeh_div": div})


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
