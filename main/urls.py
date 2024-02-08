from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='main-home'),
    path('services/', service, name='services'),
    path('contact/', contact, name='contact'),
    path('shop/', shop, name='shop'),
    path('freight-services/', single_service, name='freight-services'),
    path('shipping/create/', create_shipping, name='create-shipping'),
    path('tracking/', tracking, name='tracking'),
    path('tracking/result/', tracking_result, name='tracking-result'),
]
