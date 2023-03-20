from django.urls import path
from . import views
#from dashboard.dash_apps.finished_apps import covidDashboard
#from dashboard.dash_apps.finished_apps.readPostgresTables import covid_data
#from dashboard.dash_apps.finished_apps.dropdownPieLineMap import *

urlpatterns = [
    path('', views.cases, name = 'cases'),
    path('vaccines/', views.vaccinesAnalysis, name = 'vaccinesAnalysis'),
    path('deathRace/', views.deathRace, name = 'deathRace'),
    path('data/', views.data, name = 'data'),
    path('contact/', views.contact, name = 'contact'),
]
