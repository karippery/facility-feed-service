from rest_framework import serializers
from feed_service.models import Facility


class FacilitySerializer(serializers.ModelSerializer):
    """Serializer for Facility model, handling data conversion for API endpoints."""
    class Meta:
        model = Facility
        fields = '__all__'
