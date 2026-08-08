from rest_framework import serializers

from .models import DiscountCategory


class DiscountCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCategory
        fields = ('id', 'title', 'discount_percent')