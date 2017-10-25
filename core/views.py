
from django.shortcuts import render
from django.views import generic
from rest_framework import viewsets
from django.http import HttpResponse
from django.utils import timezone

from .models import Event, User, Tag, Join
from .forms import EventForm
from .serializers import EventSerializer

import json

class MapView(generic.View):
    context = {
        "tags": Tag.objects.all(),
        "event_list": Event.objects.order_by('start_date_time')[:3]
        }

    def post(self, request):
        form = EventForm(request.POST)
        print(form.fields.keys())

        if form.is_valid():
            # e = Event(**form.cleaned_data)
            form.save()
            # form.save_m2m()
            # Event.objects.create(**form.cleaned_data)
            self.context['state'] = "saved"
        else:
            self.context['state'] = "error"
            self.context['errors'] = form.errors

        self.context['form'] = EventForm()
        return render(request, 'core/pages/map.html', context=self.context)

    def get(self, request, *args, **kwargs):
        self.context['state'] = "get"
        self.context['form'] = EventForm()
        return render(request, 'core/pages/map.html', context=self.context)


class EventsView(generic.ListView):
    template_name = 'core/pages/events.html'
    model = Event

    def get_context_data(self, **kwargs):
        context = super(EventsView, self).get_context_data(**kwargs)
        context['fields'] = Event._meta.get_fields()
        return context

class EventJoinView(generic.View):

    def post(self, request, *args, **kwargs):
        event_id = self.kwargs['event_id']
        user_id = request.POST['user_id']

        data = {}

        try:
            user = User.objects.get(pk=user_id)
            event = Event.objects.get(pk=event_id)
            join_date = timezone.now

            Join.objects.create(user=user, event=event, join_date=join_date)

            data['result'] = True

            print("{} joined {} ({})".format(user, event, j))
            
        except Exception as e:
            print(str(e))
            data['result'] = False
        
        return HttpResponse(json.dumps(data))
        #user_id = 

class EventView(generic.DetailView):
    template_name = 'core/pages/event.html'
    model = Event

class ProfileView(generic.ListView):
    template_name = 'core/pages/profile.html'
    model = User


# Enables access to all events
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
