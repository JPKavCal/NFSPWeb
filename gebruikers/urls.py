from django.urls import path
from . import views, models

# SET THE NAMESPACE!
app_name = 'UserHandler'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='logout'),
]
