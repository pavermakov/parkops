from decimal import Decimal

from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.guests.models import Guest
from apps.tickets.models import Ticket

from .serializers import TicketPriceSerializer, TicketPurchaseSerializer

DAILY_TICKET_PRICE = Decimal('59.99')

class TicketPriceView(APIView):
    def get(self, request):
        serializer = TicketPriceSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        date_from = data.get('date_from')
        date_to = data.get('date_to', timezone.now().date())
        discount = data.get('discount')

        duration_days = (date_to - date_from).days or 1
        price = DAILY_TICKET_PRICE * duration_days

        if discount:
            price *= (1 - Decimal(discount.discount_percent) / 100)

        return Response({ 'price': price }, status.HTTP_200_OK)


class PurchaseTicketView(APIView):
    def post(self, request):
        serializer = TicketPurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        guest = validated_data.get('guest')

        # TODO: good place to wrap into transaction?
        if not guest:
            guest = Guest.objects.create(
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                height_cm=validated_data.get('height_cm'),
            )

        new_ticket = Ticket.objects.create(
            guest=guest,
            valid_from=validated_data.get('valid_from'),
            valid_to=validated_data.get('valid_to'),
            price=validated_data.get('price')
        )

        return Response(
            data={
                'success': True,
                'ticket_id': new_ticket.id
            },
            status=status.HTTP_201_CREATED
        )

