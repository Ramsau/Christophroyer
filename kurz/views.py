from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

import os

from .video import createVideo
from .models import Clip

def main(request):
    # get clip from url parameter
    vid = request.GET.get('vid')
    try:
        clip = Clip.objects.get(id=vid.split('.')[0])
    except (Clip.DoesNotExist, AttributeError):
        clip = None

    return render(request, 'kurz.html', {'clip': clip})

def requestVideo(request):
    if request.method != 'POST':
        return HttpResponse(_('Method forbidden'), status=403)

    text = request.POST.get('text')[:255]  # cut text to its max size
    vid = createVideo(text)

    return HttpResponse(vid, status=200)

def createSnippets(request):
    return main(request)


    newWordSource = '/home/christoph/Documents/christophroyer/Kurz/words'
    files = []
    for (dirpath, dirnames, filenames) in os.walk(newWordSource):
        files = filenames
        break

    files = [file for file in files if not os.path.exists(os.path.join(settings.KURZ_WORDS, file))]
    if request.method == 'GET':
        filename = files[0]
        return render(request, 'createSnippets.html', {'filename': filename})
    else:
        filename = request.POST.get('filename')
        keep = request.POST.get('keep')

        if keep == 'false':
            print('deleting ' + filename)
            os.remove(os.path.join(newWordSource, filename))
        else:
            print('keeping ' + filename)
            os.rename(
                os.path.join(newWordSource, filename),
                os.path.join(settings.KURZ_WORDS, filename)
            )

        files.remove(filename)
        print('%d files left' % len(files))

        new_filename = files[0]
        return HttpResponse(new_filename)
