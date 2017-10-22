
from django.shortcuts import render
from django.views import     generic
from django.core import      serializers
from .models import          Event, User
import                       json

class MapView(generic.ListView):
    template_name = 'core/map.html'
    
    def get_queryset(self):
        return Event.objects.order_by('-start_date_time').reverse()


class EventsView(generic.ListView):
    template_name = 'core/events.html'
    model = Event


class ProfileView(generic.ListView):
    template_name = 'core/profile.html'
    model = User
