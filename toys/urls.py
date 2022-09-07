from django.urls import path

import toys.views as v

urlpatterns = [
    path('nrla-kekse', v.nrlaKekse, name='cookies'),
    path('remote-boot/set', v.setRemoteBoot, name='setRemoteBoot'),
    path('remote-boot/upload-img', v.uploadImage, name='uploadImage'),
    path('remote-boot/bootImage.jpg', v.showImage, name='showImage'),
    path('remote-boot/<uuid:key>', v.remoteBoot, name='viewRemoteBoot'),
]

