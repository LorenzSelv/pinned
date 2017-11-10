
from django.shortcuts import render, redirect
from django.views import generic
from rest_framework import viewsets
from django.http import HttpResponse
from django.utils import timezone
from django.db.utils import IntegrityError

from .models import Event, User, Tag, Join
from .forms import EventForm
from .serializers import EventSerializer

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import json


login_decorator = login_required(login_url='/', redirect_field_name=None)


def login(request):
    return render(request, 'core/pages/login.html')


class MapView(generic.View):
    context = {
        "tags": Tag.objects.all(),
        "event_list": Event.objects.order_by('start_date_time')[:3]
        }

    @method_decorator(login_decorator)
    def post(self, request):
        # form = EventForm(request.POST, initial={'event_owner': request.user.id})

        try:
            form_temp = EventForm(request.POST)
            form = form_temp.save(commit=False)
            form.event_owner = request.user
            form.save()
            form_temp.save_m2m() # Needed for saving tags, added by using "commit=False"
            self.context['state'] = "saved"
        except ValueError as e:
            self.context['state'] = "error"
            self.context['errors'] = form_temp.errors
            self.context['other_errors'] = form_temp.non_field_errors()
            print(e)

        self.context['form'] = EventForm()
        return render(request, 'core/pages/map.html', context=self.context)

    # TODO allow to see events without login
    @method_decorator(login_decorator)
    def get(self, request, *args, **kwargs):
        # print('SESSION\n', request.session.items())
        # print('REQUEST\n', str(request.user.first_name))
        self.context['state'] = "get"
        self.context['form'] = EventForm()
        return render(request, 'core/pages/map.html', context=self.context)


@method_decorator(login_decorator, name='get')
class EventsView(generic.ListView):
    template_name = 'core/pages/events.html'
    model = Event

    def get_context_data(self, **kwargs):  # Add field names to the context
        context = super(EventsView, self).get_context_data(**kwargs)
        joined_events = {}
        user_id = self.request.user.id
        for event in context['event_list']:
            exists = Join.objects.filter(user__pk=user_id, event__pk=event.id).exists()
            if exists:
                joined_events[event.id] = True
        context['fields'] = Event._meta.get_fields()
        context['joined_events'] = joined_events
        return context


class EventJoinView(generic.View):

    @method_decorator(login_decorator)
    def post(self, request, *args, **kwargs):
        event_id = self.kwargs['event_id']
        data = {}

        try:
            event = Event.objects.get(pk=event_id)
            join_date = timezone.now
            n_participants = len(event.participants.all())

            if n_participants >= event.max_num_participants: 
                raise IntegrityError("max_num_participants reached")
            else:
                Join.objects.create(user=request.user, event=event, join_date=join_date)

            data['result'] = True
            data['participants'] = [p.first_name for p in event.participants.all()]

            print("{} joined {}".format(request.user, event))

        except IntegrityError as e:
            print("[Warning] Exception during join")
            print(str(e))
            data['result'] = False
        
        return HttpResponse(json.dumps(data))


class EventLeaveView(generic.View):

    @method_decorator(login_decorator)
    def post(self, request, *args, **kwargs):
        event_id = self.kwargs['event_id']
        data = {}

        try:
            event = Event.objects.get(pk=event_id)

            Join.objects.filter(user=request.user, event=event).delete()

            data['result'] = True
            data['participants'] = [p.first_name for p in event.participants.all()]
            print("{} left {}".format(request.user, event))

        except IntegrityError as e:
            print("[Warning] Exception during leave")
            print(str(e))
            data['result'] = False

        return HttpResponse(json.dumps(data))


@method_decorator(login_decorator, name='get')
class EventView(generic.DetailView):
    template_name = 'core/pages/event.html'
    model = Event

    def get_context_data(self, **kwargs):
        user_id = self.request.user.id
        context = super(EventView, self).get_context_data(**kwargs)
        context['joined'] = Join.objects.filter(user__pk=user_id, event__pk=self.kwargs['pk']).exists()
        return context    


@method_decorator(login_decorator, name='get')
class ProfileView(generic.DetailView):
    
    template_name = 'core/pages/profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user

        joined_events_id = list(Join.objects.filter(user=user).values_list('event', flat=True))
        # print(joined_events_id)
        joined_events = list(Event.objects.filter(id__in=joined_events_id))
        # print(joined_events)
        owned_events  = list(Event.objects.filter(event_owner=user))
        # print(owned_events)
        auth0user = user.social_auth.get(provider="auth0")
        user.picture = auth0user.extra_data['picture']
        user.email = user.username + '@gmail.com'

        tags = Tag.objects.all()

        context = {'user': user,
                   'joined_events': joined_events,
                   'owned_events': owned_events,
                   'tags': tags}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # uid = self.kwargs['pk']
        # user = User.objects.get(pk=uid)

        data = {}

        return HttpResponse(json.dumps(data))


# Enables access to all events
# @method_decorator(login_decorator)
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
