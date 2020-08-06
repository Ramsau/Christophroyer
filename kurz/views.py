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

def createSnippets(request):
    if request.method == 'GET':
        for (dirpath, dirnames, filenames) in os.walk(settings.KURZ_WORDS):
            filenames = filenames
            break

        filename = [f for f in filenames if '-' in f][0]
        return render(request, 'createSnippets.html', {'filename': filename})
    else:
        old_filename = request.POST.get('old_filename')
        new_filename = request.POST.get('new_filename')

        if not request.POST.get('pick'):
            print(old_filename, new_filename)

            if not os.path.exists(os.path.join(settings.KURZ_WORDS, new_filename)):
                os.rename(
                    os.path.join(settings.KURZ_WORDS, old_filename),
                    os.path.join(settings.KURZ_WORDS, new_filename),
                )
            else:
                return HttpResponse('?%s|%s' % (old_filename, new_filename), status=200)
        else:
            pick = request.POST.get('pick')

            if pick == 'new':
                print('overwriting %s with %s' % (old_filename, new_filename))
                os.rename(
                    os.path.join(settings.KURZ_WORDS, new_filename),
                    os.path.join(settings.KURZ_WORDS, old_filename),
                )
            else:
                print('deleting %s, leaving %s' % (new_filename, old_filename))
                os.remove(os.path.join(settings.KURZ_WORDS, new_filename))

        for (dirpath, dirnames, filenames) in os.walk(settings.KURZ_WORDS):
            filenames = filenames
            break

        filename = [f for f in filenames if '-' in f][0]

        return HttpResponse(filename, status=200)
