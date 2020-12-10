from django.urls import path

import toys.views as v

urlpatterns = [
    path('nrla-kekse', v.nrlaKekse),
]