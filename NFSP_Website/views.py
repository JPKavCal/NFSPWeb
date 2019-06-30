from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'NFSP_Website/index.html')


def team(request):
    return render(request, 'NFSP_Website/team.html')

def projects(request):
    return render(request, 'NFSP_Website/projects.html')
