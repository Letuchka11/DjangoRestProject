from .views import *
from django.urls import path, include

urlpatterns = [
    path('registration/', registration_view ),
    path('authentication/', authentication_view)
]
