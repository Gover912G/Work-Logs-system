from django.urls import path

from . import views

app_name = "logs"
urlpatterns = [
path('', views.index, name='dashboard'),  
path('add/', views.addLog, name='addLog'),
path('view/', views.viewLogs, name='viewLogs'),
path('reports/', views.reports, name='reports'),
path('export-excel/', views.export_excel, name='export_excel'),
path('export-pdf/', views.export_pdf, name='export_pdf'),
]