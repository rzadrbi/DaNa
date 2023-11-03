from admin_notification.views import check_notification_view
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('check/notification', check_notification_view, name="check_notifications"),
    path('', include('home.urls')),
    path('', include('account.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
