
from django.shortcuts import render
from django.views import generic
from rest_framework import viewsets
from django.http import HttpResponse
from django.utils import timezone
from django.db.utils import IntegrityError

from .models import Event, User, Tag, Join
from .forms import EventForm
from .serializers import EventSerializer

from django.contrib.auth.decorators import login_required

import json


def login(request):
    return render(request, 'core/pages/login.html')


class MapView(generic.View):
    context = {
        "tags": Tag.objects.all(),
        "event_list": Event.objects.order_by('start_date_time')[:3]
        }

    @login_required
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
            self.context['other_errors'] = form.non_field_errors()
            # print(other_errors)
            # print(type(other_errors))

        self.context['form'] = EventForm()
        return render(request, 'core/pages/map.html', context=self.context)

    # TODO allow to see events without login
    # @login_required
    def get(self, request, *args, **kwargs):
        self.context['state'] = "get"
        self.context['form'] = EventForm()
        return render(request, 'core/pages/map.html', context=self.context)


class EventsView(generic.ListView):
    template_name = 'core/pages/events.html'
    model = Event

    def get_context_data(self, **kwargs): # Add field names to the context
        context = super(EventsView, self).get_context_data(**kwargs)
        user_id = 1
        joined_events = {}
        for event in context['event_list']:
            exists = Join.objects.filter(user__pk=user_id, event__pk=event.id).exists()
            if exists:
                joined_events[event.id] = True
        context['fields'] = Event._meta.get_fields()
        context['joined_events'] = joined_events
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
            n_participants = len(event.participants.all())

            if n_participants >= event.max_num_participants: 
                raise IntegrityError("max_num_participants reached")
            else:
                Join.objects.create(user=user, event=event, join_date=join_date)

            data['result'] = True

            print("{} joined {}".format(user, event))

        except IntegrityError as e:
            print("[Warning] Exception during join")
            print(str(e))
            data['result'] = False
        
        return HttpResponse(json.dumps(data))


class EventView(generic.DetailView):
    template_name = 'core/pages/event.html'
    model = Event

    def get_context_data(self, **kwargs):
        user_id = 1 # Change to dynamic user
        context = super(EventView, self).get_context_data(**kwargs)
        context['joined'] = Join.objects.filter(user__pk=user_id, event__pk=self.kwargs['pk']).exists()
        return context    


class ProfileView(generic.ListView):
    template_name = 'core/pages/profile.html'
    model = User


# Enables access to all events
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
