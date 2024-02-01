from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='main-home'),
    path('services/', service, name='services'),
    path('single-services/', single_service, name='single-services'),
]
