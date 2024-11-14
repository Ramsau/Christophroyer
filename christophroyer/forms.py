from django import forms
from django.utils.translation import gettext_lazy as _, gettext as gt
from django.utils.safestring import mark_safe
from django.utils.functional import lazy

from django.urls import reverse_lazy, reverse

class RequestForm(forms.Form):
    name = forms.CharField(label=_('Name*'), widget=forms.TextInput)
    mail = forms.CharField(label=_('Email*'), widget=forms.EmailInput)
    tel = forms.CharField(label=_('Phone'), required=False, widget=forms.TextInput)
    title = forms.CharField(label=_('Project idea*'), widget=forms.TextInput)
    text = forms.CharField(label=_('Description*'), widget=forms.Textarea)
    copy = forms.BooleanField(label=_('Send copy to me'), required=False)
    tos = forms.BooleanField(label=lazy(
        lambda: mark_safe(_('I agree with the <a href="{0}">Terms of service</a>*').format(reverse('privacy'))),
        str
        )()
    )

