from django.urls import path

from . import views

app_name = "logs"
urlpatterns = [
path('', views.index, name='dashboard'),  
path('add/', views.addLog, name='addLog'),
path('view/', views.viewLogs, name='viewLogs'),
path('reports/', views.reports, name='reports'),
]