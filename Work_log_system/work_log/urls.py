from django.urls import path

from . import views

app_name = "logs"
urlpatterns = [
path('', views.index, name='dashboard'),  
path('add/', views.addLog, name='addLog'),
]