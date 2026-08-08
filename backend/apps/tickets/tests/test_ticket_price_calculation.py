from datetime import timedelta

from django.utils import timezone

from apps.discounts.models import DiscountCategory

from ..services import DAILY_TICKET_PRICE, calculate_ticket_price


def test_passes_single_day_no_discount():
    data = { 'date_from': timezone.now().date() }
    price = calculate_ticket_price(data)

    assert price == DAILY_TICKET_PRICE


def test_passes_single_day_with_discount():
    data = {
        'date_from': timezone.now().date(),
        'discount': DiscountCategory(title="Discount", discount_percent=50)
    }

    price = calculate_ticket_price(data)
    assert price == DAILY_TICKET_PRICE / 2


def test_passes_multi_day_no_discount():
    days = 2
    data = {
        'date_from': timezone.now().date(),
        'date_to': (timezone.now() + timedelta(days=days)).date()
    }

    price = calculate_ticket_price(data)
    assert price == DAILY_TICKET_PRICE * days


def test_passes_multi_day_with_discount():
    days = 2
    data = {
        'date_from': timezone.now().date(),
        'date_to': (timezone.now() + timedelta(days=days)).date(),
        'discount': DiscountCategory(title="Discount", discount_percent=50)
    }

    price = calculate_ticket_price(data)
    assert price == (DAILY_TICKET_PRICE * days) / 2
