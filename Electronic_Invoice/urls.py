from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('home.urls')),
    url(r'^invoice_fe/', include('invoice_fe.urls')),
    url(r'^company/', include('company.urls')),
    url(r'^client/', include('client.urls')),
    url(r'^employee/', include('employee.urls')),
    url(r'^inventory/', include('inventory.urls')),
    url(r'^api/', include('api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)