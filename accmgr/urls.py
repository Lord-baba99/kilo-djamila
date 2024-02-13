from django.urls import path
from . views import *

urlpatterns = [
    path('login/', login_user, name='login'),
    path('signup/', signup, name='signup'),
    #path('teacher-signup/', signup_teacher, name='teacher-signup'),
    path('logout/', logout_user, name='logout'),
    # path('make-teacher-request/', make_request, name='make-teacher-request'),
    # path('settings/', settings, name='account-settings'),
    path('reset-password/', reset_password, name='reset-password'),
]
