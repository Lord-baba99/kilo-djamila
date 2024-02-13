from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from main import urls as main_urls
from accmgr import urls as acc_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include(main_urls)),
    path('account/', include(acc_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)