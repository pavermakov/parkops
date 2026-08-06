from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.attractions.models import Attraction
from apps.tickets.models import Ticket
from apps.turnstile.services import (
    RideClosedError,
    TicketScanError,
    check_attraction_status,
    check_ticked_purchased_today,
)

from .serializers import ScanTicketSerializer


class ScanTicketView(APIView):
    def post(self, request):
        serializer = ScanTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attraction = get_object_or_404(Attraction, pk=serializer.validated_data['attraction_id'])
        ticket = get_object_or_404(Ticket, pk=serializer.validated_data['ticket_id'])
        
        try:
            check_ticked_purchased_today(ticket)
            check_attraction_status(attraction)
        except (TicketScanError, RideClosedError) as err:
            return Response({"error": err.message}, status=status.HTTP_409_CONFLICT)

        return Response(
            {"success": f"Enjoy your ride on {attraction.name}!"},
            status=status.HTTP_200_OK,
        )





