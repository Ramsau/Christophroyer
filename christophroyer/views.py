import christophroyer.models as m
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _, ugettext as gt

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
            mail_html = render_to_string('mail_commission.html', data)
            mail_text = '''
                %s: %s
                %s(%s) %s
                %s
                %s
                
                %s
            ''' % (
                _('Project request'), data['title'],
                data['name'], data['mail'] + '/' + data['tel'] if data['tel'] else data['mail'],
                _('proposed the following project:'),
                data['title'],
                data['text'],
                _('This message was sent from christophroyer.com - If you didn\'t use this website, tell me via E-Mail '
                  '(mail@christophroyer.com) and I will discard your information')
            )

            try:
                mail = EmailMultiAlternatives(
                    gt('Project request') + ': ' + data.get('title'),
                    mail_text,
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_REQUEST_RECIPIENT],
                    reply_to=[data['mail']]
                )
                mail.attach_alternative(mail_html, 'text/html')
                mail.send()

                if data.get('copy') == 'on':
                    mail_copy = EmailMultiAlternatives(
                        gt('Project request') + ': ' + data.get('title') + '(' + gt('Copy') + ')',
                        mail_text,
                        settings.EMAIL_HOST_USER,
                        [data['mail']],
                        reply_to=[settings.EMAIL_REQUEST_RECIPIENT]
                    )
                    mail_copy.attach_alternative(mail_html, 'text/html')
                    mail_copy.send()
            except:
                return HttpResponse(_('Error while sending mail, please try again later'), status=500)

            return HttpResponse(_('Your request was sent - I\'ll get in touch soon!'))
        else:
            return HttpResponse(_('Invalid data - please check your inputs for errors'), status=400)
