from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TicketPriceSerializer, TicketPurchaseSerializer
from .services import calculate_ticket_price, create_new_ticket


class TicketPriceView(APIView):
    def get(self, request):
        serializer = TicketPriceSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        return Response(
            data={
                'price': calculate_ticket_price(serializer.validated_data)
            },
            status=status.HTTP_200_OK
        )


class PurchaseTicketView(APIView):
    def post(self, request):
        serializer = TicketPurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            data={
                'success': True,
                'ticket_id': create_new_ticket(serializer.validated_data).id
            },
            status=status.HTTP_201_CREATED
        )

