from django.shortcuts import render
from django.http import HttpResponse

import christophroyer.models as m


def index(request):
    return render(request, 'index.html')


def projects(request):
    projects = m.Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})

def commissions(request):
    if request.method == 'GET':
        return render(request, 'commissions.html')
