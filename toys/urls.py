from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import toys.views as v

urlpatterns = [
    path('nrla-kekse', v.nrlaKekse, name='cookies'),
    path('remote-boot/set', v.setRemoteBoot, name='setRemoteBoot'),
    path('remote-boot/upload-img', v.uploadImage, name='uploadImage'),
    path('remote-boot', v.remoteBoot, name='viewRemoteBoot'),
]

urlpatterns += static('remote-boot/bootImage/', document_root=settings.REMOTE_BOOT_IMAGE_PATH)
