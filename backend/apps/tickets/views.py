from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tickets.models import Ticket

from .serializers import TicketPurchaseSerializer


class PurchaseTicketView(APIView):
    def post(self, request):
        serializer = TicketPurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_ticket = Ticket.objects.create(**serializer.validated_data)

        return Response({ 'success': True, 'ticket_id': new_ticket.id }, status=status.HTTP_200_OK)