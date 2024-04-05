from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='main-home'),
    path('services/', service, name='services'),
    path('contact/', contact, name='contact'),
    path('shop/', shop, name='shop'),
    path('about-us/', about_us, name='about-us'),
    path('articles/<int:category_id>/', get_article, name='articles'),
    path('ocean-freight-services/', ocean_freight_service, name='ocean-freight-services'),
    path('air-freight-services/', air_freight_service, name='air-freight-services'),
    path('shipping/create/', create_shipping, name='create-shipping'),
    path('tracking/', tracking, name='tracking'),
    path('tracking/result/', tracking_result, name='tracking-result'),
]
