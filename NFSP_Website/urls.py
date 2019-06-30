from django.urls import path
from . import views

# SET THE NAMESPACE!
app_name = 'NFSP_Website'

urlpatterns = [
    path('', views.index, name='home'),
    path('team/', views.team, name='team'),
    path('projects/', views.projects, name='projects'),
]
