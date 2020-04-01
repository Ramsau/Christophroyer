from django.shortcuts import render

import christophroyer.models as m


def index(request):
    return render(request, 'index.html')


def privacy(request):
    return render(request, 'privacy.html')


def projects(request):
    projects = m.Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})


def commissions(request):
    if request.method == 'GET':
        return render(request, 'commissions.html')
