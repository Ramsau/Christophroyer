"""christophroyer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.urls import path, include

import christophroyer.views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.index, name='index'),

    path('i18n/', include('django.conf.urls.i18n'), name='set_language'),
    path('kurz/', include(('kurz.urls', 'kurz'), namespace='kurz')),
]

urlpatterns += i18n_patterns(
    path(_('Privacy'), v.privacy, name='privacy'),
    path(_('Projects'), v.projects, name='projects'),
    path(_('Commissions'), v.commissions, name='commissions')
)
