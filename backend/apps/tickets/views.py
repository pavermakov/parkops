from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.guests.models import Guest
from apps.tickets.models import Ticket

from .serializers import TicketPurchaseSerializer


class PurchaseTicketView(APIView):
    def post(self, request):
        serializer = TicketPurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        guest = data.pop('guest', None)

        if guest is None:
            guest = Guest.objects.create(
                first_name=data.pop('first_name'),
                last_name=data.pop('last_name'),
                height_cm=data.pop('height_cm'),
            )
        else:
            data.pop('first_name', None)
            data.pop('last_name', None)
            data.pop('height_cm', None)

        new_ticket = Ticket.objects.create(guest=guest, **data)
        response = { 'success': True, 'ticket_id': new_ticket.id }

        if guest:
            response['guest_id'] = guest.id

        return Response(response, status=status.HTTP_200_OK)