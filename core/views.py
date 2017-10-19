from django.http import HttpResponse

from django.views import generic
from .models import Event, User


class MapView(generic.View):
    # TODO verify
    # template_name = 'core/map.html'

    def get(self, request, *args, **kwargs):
        return HttpResponse("<h2> Map.. </h2>")


class EventsView(generic.ListView):
    template_name = 'core/events.html'
    model = Event


class ProfileView(generic.ListView):
    template_name = 'core/profile.html'
    model = User
