
from django.shortcuts import render
from django.views import generic
from .models import Event, User, Tag

# class MapView(generic.ListView):
#     template_name = 'core/map.html'
#
#     def get_queryset(self):
#         return Event.objects.order_by('-start_date_time').reverse()
# =======


class MapView(generic.View):

    def get(self, request, *args, **kwargs):
        context = {"tags": Tag.objects.all(),
                   "event_list" :Event.objects.order_by('-start_date_time').reverse()
                   }
        return render(request, 'core/pages/map.html', context=context)


class EventsView(generic.ListView):
    template_name = 'core/pages/events.html'
    model = Event


class ProfileView(generic.ListView):
    template_name = 'core/pages/profile.html'
    model = User
