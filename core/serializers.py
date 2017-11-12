from .models import Event, Tag, User
from rest_framework import serializers


# Serializer that prepares data about the tags for the api endpoint
class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'color')


# Serializer that prepares data for the api endpoint
class EventSerializer(serializers.HyperlinkedModelSerializer):
    tag_code = serializers.SerializerMethodField('get_tag')

    def get_tag(self, obj):
        return obj.tag.html()

    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'latitude', 'longitude', 'tag_code')


# Serializer that prepares data about the users for the api endpoint
class UserSerializer(serializers.HyperlinkedModelSerializer):
    interest_tags = serializers.SerializerMethodField('get_tags')

    def get_tags(self, obj):
        return (tag.name for tag in obj.interest_tags.all())

    class Meta:
        model = User
        fields = ('username', 'email', 'followers', 'interest_tags')