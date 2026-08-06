from decimal import Decimal

from django.utils import timezone
from rest_framework import serializers

from apps.guests.models import Guest


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

        if not guest:
            missing_guest_info = [field for field in ['first_name', 'last_name', 'height_cm'] if field not in attrs]

            if missing_guest_info:
                raise serializers.ValidationError(f'guest_id or {", ".join(missing_guest_info)} required')

        if valid_from < timezone.now().date():
            raise serializers.ValidationError('valid_from must be today or later')

        if valid_to and valid_to < attrs['valid_from']:
            raise serializers.ValidationError({
                'valid_to': 'valid_to must be greater than or equal to valid_from.'
            })

        return attrs
