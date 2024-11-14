from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.static import serve

import os
from django.conf import settings
import datetime
import toys.models as m

@login_required
def setRemoteBoot(request):
    if request.method == 'GET':
        return render(request, 'remoteBoot.html')
    else:
        token = get_object_or_404(m.BootToken, user=request.user)
        command = request.POST.get('set')
        if command in ['Linux', 'LinuxVNC', 'Windows', 'TakeImage', 'ForceShutdown']:
            m.BootSignal.objects.create(ip=request.META.get('REMOTE_ADDR'), type=command, token=token)
            return HttpResponse('set')
        else:
            return HttpResponse('Invalid command: ' + command, status=400)


def remoteBoot(request, key):
    # check if a boot signal is younger than a minute
    token = get_object_or_404(m.BootToken, key=key)
    newestSignal = m.BootSignal.objects.filter(token=token).order_by('-timestamp').first()
    if datetime.datetime.now() - newestSignal.timestamp.replace(tzinfo=None) < datetime.timedelta(minutes=1):
        return HttpResponse(newestSignal.type)
    else:
        return HttpResponse('Do not turn it on')


@csrf_exempt
def uploadImage(request):
    if not request.method == 'POST':
        return HttpResponse('Method not allowed', status=405)

    if request.POST.get('secretString', '') == settings.REMOTE_BOOT_SECRET:
        if request.FILES.get('img'):
            with open(os.path.join(settings.REMOTE_BOOT_IMAGE_PATH, 'img.jpg'), 'wb+') as dest:
                for chunk in request.FILES['img']:
                    dest.write(chunk)
            return HttpResponse('Done')
        else:
            return HttpResponse('No Image provided', status=400)
    else:
        return HttpResponse('Unauthorized', status=401)


def showImage(request):
    return serve(request, 'img.jpg', settings.REMOTE_BOOT_IMAGE_PATH)
