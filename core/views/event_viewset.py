from datetime import datetime
from django.utils import timezone
from django.utils import dateparse

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Event, User, Tag
from ..serializers import EventSerializer


class EventViewSet(APIView):

    def get(self, request, *args, **kwargs):
        # Get all events that have not ended yet
        queryset = Event.objects.filter(end_date_time__gt=timezone.now())

        # Obtain the list of user scopes (interests, single tag, text filtering and date filtering)
        scopes = request.GET.getlist('scopes[]')
        
        # Filter on user's interests
        if 'interests' in scopes:
            user_id = request.user.id
            user = User.objects.get(pk=user_id)
            tags = user.interest_tags.all()

            queryset = queryset.filter(tag__in=tags)

        # Filter to just one tag
        elif 'tag' in scopes:
            selected_tag = request.GET['tag']
            tag = Tag.objects.get(name=selected_tag)

            queryset = queryset.filter(tag=tag)

        # Filter by text contained in event name
        if 'name' in scopes:
            text = request.GET['text']

            queryset = queryset.filter(name__icontains=text)
        
        # Filter by start date
        if 'date' in scopes:
            date = request.GET['date']
            datetime_object = timezone.make_aware(datetime.strptime(date, '%m/%d/%y'))

            queryset = queryset.filter(start_date_time__gt=datetime_object)

        serializer_class = EventSerializer(queryset, many=True, context={'request': request})

        return Response(serializer_class.data)