from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
import os
from django.conf import settings
import base64
import datetime
import fitz
from PIL import Image, ImageEnhance
import toys.models as m


def nrlaKekse(request):
    if request.method == 'GET':
        return render(request, 'nrlaKekse.html')
    else:
        timestamp = datetime.datetime.now().timestamp()
        main_pdf = os.path.join(settings.STATICFILES_DIRS[0], 'div/nrla_blatt.pdf')
        pdf_dims = (600, 848)

        mimeType = request.POST['img'].split('/')[1].split(';')[0]

        if not mimeType in ['png', 'jpeg']:
            return HttpResponse('Bitte .png oder .jpeg-Fotos hochladen', status=400)

        res_pdf = os.path.join(settings.MEDIA_ROOT, 'nrla-kekse', str(timestamp) + '.pdf')
        bg_img = res_pdf + '.' + mimeType

        # discard mimetype-header, write image to file
        img_binary = base64.b64decode(request.POST['img'].split(',')[1])
        with open(bg_img, 'wb') as f:
            f.write(img_binary)

        # whiten image
        img = Image.open(bg_img)
        img = ImageEnhance.Contrast(img).enhance(0.3)
        img = ImageEnhance.Brightness(img).enhance(1.5)

        if img.width > img.height:
            img = img.transpose(Image.ROTATE_90)

        img.save(bg_img)

        # calculate image proportions/position
        prop_width = (float(img.width) / float(img.height)) * pdf_dims[1]
        prop_left = (pdf_dims[0] - prop_width) / 2

        # set as background
        doc = fitz.open(main_pdf)

        rect = fitz.Rect(prop_left, 0, pdf_dims[0] - prop_left, pdf_dims[1])
        pix = fitz.Pixmap(bg_img)

        for page in doc:
            page.insertImage(rect, pixmap=pix, overlay=False)

        doc.save(res_pdf)

        # read to b64 string
        with open(res_pdf, 'rb') as f:
            resp_data = base64.b64encode(f.read())

        # clean up crime scene
        os.remove(res_pdf)
        os.remove(bg_img)

        return HttpResponse(resp_data)


@login_required
def setRemoteBoot(request):
    if request.method == 'GET':
        return render(request, 'remoteBoot.html')
    else:
        command = request.POST.get('set')
        if command == 'Linux':
            m.BootSignal.objects.create(ip=request.META.get('REMOTE_ADDR'), type='Linux')
        elif command == 'Windows':
            m.BootSignal.objects.create(ip=request.META.get('REMOTE_ADDR'), type='Windows')
        return HttpResponse('set')

def remoteBoot(request):
    # check if a boot signal is younger than a minute
    newestSignal = m.BootSignal.objects.order_by('-timestamp').first()
    if datetime.datetime.now() - newestSignal.timestamp.replace(tzinfo=None) < datetime.timedelta(minutes=1):
        return HttpResponse('Please boot to ' + newestSignal.type + ' dear Pi')
    else:
        return HttpResponse('Do not turn it on')

