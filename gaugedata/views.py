from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import RiverGauge, Catchment, CatchForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models.functions import Substr

from bokeh.layouts import Spacer, row
from bokeh.plotting import figure
from bokeh.models import Range1d
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import ColumnDataSource, Panel, Tabs


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
                                                  'regions': region,
                                                  })


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


@login_required
def catchform(request):
    if request.method == 'POST':
        try:
            catchment = Catchment.objects.get(pk=request.POST['station'])
            form = CatchForm(instance=catchment)

            x = [2, 5, 10, 20, 50, 100, 200]
            y = [
                catchment.dr2,
                catchment.dr5,
                catchment.dr10,
                catchment.dr20,
                catchment.dr50,
                catchment.dr100,
                catchment.dr200,
            ]

            TOOLTIPS = [
                ("Year", "@x"),
                ("Rainfall Depth (mm)", "@y")
            ]

            source = ColumnDataSource(data=dict(x=x, y=y))

            plot = figure(
                title='Design Rainfall Depths',
                sizing_mode='stretch_width',
                tools=['pan', 'box_zoom', 'save',
                       'reset', 'wheel_zoom'],
                y_range=Range1d(min(y) * 0.8, max(y) * 1.1, bounds=(min(y) * 0.5, max(y) * 1.15)),
                x_range=Range1d(min(x) - 1, max(x) + 50, bounds=(min(x) - 1, max(x) + 50)),
                x_axis_type="log",
                x_axis_label="Return Period (1:x year)",
                y_axis_label="Rainfall Depth (mm)",
                # plot_width=450,
                plot_height=400,
                id='rain_fig',
                tooltips=TOOLTIPS,
                active_drag=None,
                active_scroll=None
            )
            plot.line('x', 'y', source=source)
            plot.circle(x, y, fill_color="white", size=8)
            plot.toolbar.logo = None
            t = Spacer()
            layout = row(t, plot)  # , slider

            script, div = components(layout, CDN)

        except ObjectDoesNotExist:
            form = CatchForm()
            script = "<h4>No Graph to display</h4>"
            div = ""
            y = []

        return render(request, 'gaugedata/catch_data.html', {'form': form,
                                                               'x_list': y,
                                                               "bokeh_script": script,
                                                               "bokeh_div": div
                                                             })


@login_required
def stats_data(request):

    # Define AMS panel
    x = [1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995]
    y = [3, 4, 12, 1, 5, 13, 25, 12, 6, 7]

    TOOLTIPS = [
        ("Year", "@year"),
        ("Flow", "@flow")
    ]

    source_ams = ColumnDataSource(data=dict(year=x, flow=y))

    plot_ams = figure(
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
        tooltips=TOOLTIPS,
        active_drag=None,
        active_scroll=None
    )
    plot_ams.line('year', 'flow', source=source_ams)
    plot_ams.circle('year', 'flow', source=source_ams, fill_color="white", size=8)
    plot_ams.toolbar.logo = None

    # Define FFA Panel
    xf = [2, 5, 10, 20, 50, 100, 200]
    yf = [10, 20, 50, 100, 200, 300, 400]

    TOOLTIPSf = [
        ("RP", "@rp"),
        ("Flow", "@flow")
    ]

    source_ffa = ColumnDataSource(data=dict(rp=xf, flow=yf))

    plot_ffa = figure(
        sizing_mode='stretch_width',
        tools=['pan', 'box_zoom', 'save',
               'reset', 'wheel_zoom'],
        y_range=Range1d(min(yf) * 0.8, max(yf) * 1.1, bounds=(min(yf) * 0.5, max(yf) * 1.15)),
        x_range=Range1d(min(xf) - 1, max(xf) + 50, bounds=(min(xf) - 1, max(xf) + 50)),
        x_axis_label="Return Period (1:x yr)",
        y_axis_label="Peak Flow (m³.s⁻¹)",
        x_axis_type="log",
        # plot_width=450,
        plot_height=400,
        id='stat_fig2',
        tooltips=TOOLTIPSf,
        active_drag=None,
        active_scroll=None
    )
    plot_ffa.line('rp', 'flow', source=source_ffa)
    plot_ffa.circle('rp', 'flow', source=source_ffa, fill_color="white", size=8)
    plot_ffa.toolbar.logo = None

    t = Spacer()
    tabs = Tabs(tabs=[
              Panel(child=row(plot_ffa, t), title="FFA"),
              Panel(child=row(plot_ams, t), title="AMS")
    ])

    t = Spacer()

    script, div = components(tabs, CDN)

    return render(request, 'gaugedata/stats_data.html', {
                                                  "bokeh_script": script,
                                                  "bokeh_div": div,
                                                  "xf": zip(xf, yf)
                                                  })
