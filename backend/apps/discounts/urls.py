from django.urls import path

from .views import DiscountsView

urlpatterns = [
    path('', DiscountsView.as_view())
]