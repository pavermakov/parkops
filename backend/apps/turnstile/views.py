from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ScanTicketSerializer
from .services import generate_riders_count_report, scan_ticket_at_attraction


class ScanTicketView(APIView):
    def post(self, request):
        serializer = ScanTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        attraction, err = scan_ticket_at_attraction(serializer.validated_data)

        if err:
            return Response(
                data={"error": err.message},
                status=status.HTTP_409_CONFLICT
            )

        return Response(
            data={"success": f"Enjoy your ride on {attraction.name}!"},
            status=status.HTTP_200_OK,
        )

class ReportRidersCount(APIView):
    def get(self, request):
        return Response(
            data=generate_riders_count_report(),
            status=status.HTTP_200_OK
        )