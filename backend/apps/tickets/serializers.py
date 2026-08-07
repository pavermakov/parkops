from decimal import Decimal

from django.utils import timezone
from rest_framework import serializers

from apps.guests.models import DiscountCategory, Guest


class TicketPriceSerializer(serializers.Serializer):
    date_from = serializers.DateField(required=True)
    date_to = serializers.DateField(required=False)
    
    discount_id = serializers.PrimaryKeyRelatedField(
        queryset=DiscountCategory.objects.all(),
        source='discount',
        required=False
    )

    def validate(self, attrs):
        date_from = attrs.get('date_from')
        date_to = attrs.get('date_to')

        # validate ticket's start date not in the past
        if date_from < timezone.now().date():
            raise serializers.ValidationError('date_from must be today or later')

        # validate ticket's end date (if exists) is later than its start date
        if date_to and date_to < date_from:
            raise serializers.ValidationError({
                'date_to': 'date_to must be greater than or equal to date_from.'
            })

        return attrs


class TicketPurchaseSerializer(serializers.Serializer):
    guest_id = serializers.PrimaryKeyRelatedField(queryset=Guest.objects.all(), source='guest', required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    height_cm = serializers.IntegerField(required=False)
    valid_from = serializers.DateField()
    valid_to = serializers.DateField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))

    def validate(self, attrs):
        guest = attrs.get('guest')
        valid_from = attrs.get('valid_from')
        valid_to = attrs.get('valid_to')

        # validate new guest passed required data or existing guest passed their id
        if not guest:
            missing_guest_info = [field for field in ['first_name', 'last_name', 'height_cm'] if field not in attrs]

            if missing_guest_info:
                raise serializers.ValidationError(f'guest_id or {", ".join(missing_guest_info)} required')

        # validate ticket's start date not in the past
        if valid_from < timezone.now().date():
            raise serializers.ValidationError('valid_from must be today or later')

        # validate ticket's end date (if exists) is later than its start date
        if valid_to and valid_to < valid_from:
            raise serializers.ValidationError({
                'valid_to': 'valid_to must be greater than or equal to valid_from.'
            })

        return attrs
