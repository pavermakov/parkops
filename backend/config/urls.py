from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('turnstile/', include('apps.turnstile.urls')),
    path('tickets/', include('apps.tickets.urls')),
    path('discounts/', include('apps.discounts.urls')),
]
