from rest_framework import serializers


class ScanTicketSerializer(serializers.Serializer):
    attraction_id = serializers.IntegerField()
    ticket_id = serializers.IntegerField()
