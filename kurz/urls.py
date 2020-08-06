from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import kurz.views as v

urlpatterns = [
    path('', v.main, name='index'),
    path('requestVideo', v.requestVideo, name='requestVideo'),
    path('createSnippets', v.createSnippets, name='createSnippets')
]

urlpatterns += static('video/', document_root=settings.KURZ_CLIPS)
urlpatterns += static('words/', document_root=settings.KURZ_WORDS)


