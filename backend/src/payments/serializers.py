from rest_framework import serializers


class CheckoutSessionSerializer(serializers.Serializer):
    session_id = serializers.CharField()
    url = serializers.URLField()