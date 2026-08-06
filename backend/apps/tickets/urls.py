from django.urls import path

from .views import PurchaseTicketView

urlpatterns = [
    path('buy/', PurchaseTicketView.as_view())
]