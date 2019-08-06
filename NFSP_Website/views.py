from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'NFSP_Website/index.html')


def team(request):
    return render(request, 'NFSP_Website/team.html')


def projects(request):
    import csv
    from django.templatetags.static import static
    from collections import OrderedDict

    data = {}
    with open(f"./{static('nfsp/NFSP_Projects.csv')}") as f:
        t = csv.reader(f)
        for row in t:
            try:
                pnum = int(row[1])
                pri = int(row[0])
                if pri < 9:
                    badge = 'danger'
                    text = 'High'
                elif pri < 16:
                    badge = 'warning'
                    text = 'Medium'
                else:
                    badge = 'success'
                    text = 'Low'

                if row[4] == '\xa0':
                    focus = None
                else:
                    focus = row[4]
                data[pnum] = {'pri': {'badge': badge, 'text': text}, 'title': row[2], 'desc': row[3], 'focus': focus}
            except ValueError:
                continue

    keys = list(data.keys())
    keys.sort()
    data_ordered = OrderedDict()
    for key in keys:
        data_ordered[key] = data[key]

    return render(request, 'NFSP_Website/projects.html', {'data': data_ordered})


def publications(request):
    return render(request, 'NFSP_Website/publications.html')
