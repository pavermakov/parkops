from django.urls import path

from .views import ScanTicketView

urlpatterns = [
    path('scan/', ScanTicketView.as_view(), name='scan-ticket')
]