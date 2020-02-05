from django.shortcuts import render

import christophroyer.models as m


def index(request):
    return render(request, 'index.html')


def projects(request):
    projects = m.Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})
