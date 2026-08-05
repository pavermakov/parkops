from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.attractions.models import Attraction
from apps.turnstile.services import RideClosedError, check_attraction_status


class ScanTicketView(APIView):
    def post(self, request):
        attraction_id = request.data.get('attraction_id')

        try:
            attraction = get_object_or_404(Attraction, pk=attraction_id)
            check_attraction_status(attraction)
            return Response({ 'success': f'Enjoy your ride on {attraction.name}!' }, status=status.HTTP_200_OK)
        except Http404:
            return Response({ 'error': 'Ride not found' }, status=status.HTTP_404_NOT_FOUND)
        except RideClosedError as err:
            return Response({ 'error': err.message }, status=status.HTTP_409_CONFLICT)




