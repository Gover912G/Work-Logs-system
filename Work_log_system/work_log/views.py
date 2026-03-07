from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'logs/index.html', {"title": "dashboard"})

def addLog(request):
    return render(request, 'logs/addLog.html', {"title": "addLog"})