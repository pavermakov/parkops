from django.urls import path

from .views import PurchaseTicketView, TicketPriceView

urlpatterns = [
    path('price/', TicketPriceView.as_view()),
    path('buy/', PurchaseTicketView.as_view())
]