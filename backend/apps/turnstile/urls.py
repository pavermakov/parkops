from django.urls import path

from .views import ReportRidersCount, ScanTicketView

urlpatterns = [
    path('scan/', ScanTicketView.as_view(), name='scan-ticket'),
    path('report/', ReportRidersCount.as_view(), name='report-rider-count')
]