from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _, ugettext as gt
from django.conf import settings

import christophroyer.models as m
from christophroyer import forms


def index(request):
    return render(request, 'index.html')


def privacy(request):
    return render(request, 'privacy.html')


def projects(request):
    projects = m.Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})


def commissions(request):
    if request.method == 'GET':
        form = forms.RequestForm()
        return render(request, 'commissions.html', {'form': form})
    else:
        form = forms.RequestForm(request.POST)
        # send mail with the necessary details to me (and maybe a copy to user)
        if form.is_valid:
            data = form.data
            try:
                send_mail(
                    gt('Project request') + ' ' + data.get('title'),
                    data.get('name') + data.get('mail') + data.get('tel') + data.get('text'),
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_REQUEST_RECIPIENT],
                    fail_silently=False
                )
            except:
                return HttpResponse(_('Error while sending mail, please try again later'), status=500)

            return HttpResponse(_('Your request was sent - I\'ll get in touch soon!'))
        else:
            return HttpResponse(_('Invalid data - please check your inputs for errors'), status=400)
