
from django.shortcuts import render

from django.views import generic
from .models import Event, User


class MapView(generic.View):

    def get(self, request, *args, **kwargs):
        return render(request, 'core/map.html')


class EventsView(generic.ListView):
    template_name = 'core/events.html'
    model = Event


class ProfileView(generic.ListView):
    template_name = 'core/profile.html'
    model = User
