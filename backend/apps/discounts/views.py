from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DiscountCategory
from .serializers import DiscountCategorySerializer


class DiscountsView(APIView):
    def get(self, request):
        discounts = DiscountCategory.objects.all()
        serializer = DiscountCategorySerializer(discounts, many=True)

        return Response(
            { 'discounts': serializer.data },
            status=status.HTTP_200_OK
        )
