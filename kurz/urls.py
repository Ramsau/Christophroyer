from django.urls import path

import kurz.views as v

urlpatterns = [
    path('', v.main, name='index'),
    path('requestVideo', v.requestVideo, name='requestVideo'),
    path('video/<id>', v.provideVideo, name='video'),
]


