from decimal import Decimal

from django.utils import timezone
from rest_framework import serializers

from apps.guests.models import Guest


class TicketPurchaseSerializer(serializers.Serializer):
    guest_id = serializers.PrimaryKeyRelatedField(queryset=Guest.objects.all(), source='guest')
    valid_from = serializers.DateField()
    valid_to = serializers.DateField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))

    def validate(self, attrs):
        value_from = attrs.get('value_from')
        valid_to = attrs.get('valid_to')

        if value_from < timezone.now().date():
            raise serializers.ValidationError('valid_from must be today or later')

        if valid_to and valid_to < attrs['valid_from']:
            raise serializers.ValidationError({
                'valid_to': 'valid_to must be greater than or equal to valid_from.'
            })

        return attrs
