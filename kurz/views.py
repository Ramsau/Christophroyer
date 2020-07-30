from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import os

from .video import createVideo

def main(request):
    return render(request, 'kurz.html')

def requestVideo(request):
    if request.method != 'POST':
        return HttpResponse(_('Method forbidden'), status=403)

    text = request.POST.get('text')[:255]  # cut text to its max size
    vid = createVideo(text)

    return HttpResponse(vid, status=200)

def provideVideo(request, id):
    clip_path = os.path.join(settings.KURZ_CLIPS, id)
    clip_file = open(clip_path, 'rb')
    response = HttpResponse(content=clip_file)
    response['Content-Type'] = 'video/webm'
    response['Content-Disposition'] = 'attachment; filename="%s"' % id
    response['Accept-Ranges'] = 'bytes'

    return response