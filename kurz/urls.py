from django.urls import path

import kurz.views as v

urlpatterns = [
    path('', v.main)
]


