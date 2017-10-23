from .models import Event
from rest_framework import serializers

# Serializer that prepares data for the api endpoint
class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ('name', 'description', 'latitude', 'longitude')