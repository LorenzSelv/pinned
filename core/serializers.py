from .models import Event, Tag, User
from rest_framework import serializers


# Serializer that prepares data about the tags for the api endpoint
class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'color')


# Serializer that prepares data for the api endpoint
class EventSerializer(serializers.HyperlinkedModelSerializer):
    tag_names = serializers.SerializerMethodField('get_tags')

    def get_tags(self, obj):
        return (tag.name for tag in obj.tags.all())

    class Meta:
        model = Event
        fields = ('name', 'description', 'latitude', 'longitude', 'tag_names')


# Serializer that prepares data about the users for the api endpoint
class UserSerializer(serializers.HyperlinkedModelSerializer):
    interest_tags = serializers.SerializerMethodField('get_tags')

    def get_tags(self, obj):
        return (tag.name for tag in obj.interest_tags.all())

    class Meta:
        model = User
        fields = ('username', 'email', 'followers', 'interest_tags')