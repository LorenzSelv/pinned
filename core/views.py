
from django.shortcuts import render, redirect
from django.views import generic
from rest_framework import viewsets
from django.http import HttpResponse
from django.utils import timezone
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Event, User, Tag, Join, UserNotification
from .forms import EventForm
from .serializers import EventSerializer, TagSerializer, UserSerializer

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import json
import datetime


login_decorator = login_required(login_url='/', redirect_field_name=None)


def get_user_notifications(user):
    notifications = UserNotification.objects.filter(user=user)
    result = [notification.content_object for notification in notifications]
    return result


def login(request):
    if request.user.is_authenticated():
        return redirect('map/')
    return redirect('/login/auth0')


class MapView(generic.View):
    now = timezone.now()
    context = {
        "event_list": Event.objects.filter(end_date_time__gt=now, start_date_time__gt=now).filter()
                                   .order_by('start_date_time')[:3]
        }

    @method_decorator(login_decorator)
    def post(self, request):

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

    def get(self, request, *args, **kwargs):
        self.context['state'] = "get"
        if request.user.is_authenticated():
            self.context['form'] = EventForm()
            user_id = request.user.id
            user = User.objects.get(pk=user_id)
            tags = user.interest_tags.all()
            self.context['tags'] = tags
                # TODO: remove! For testing the notification
            user = User.objects.filter(username='Lorenzo')
            self.context['notifications'] = get_user_notifications(user)
            self.context.pop('not_logged_in', None)
        else:
            self.context['not_logged_in'] = True
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

        context['notifications'] = get_user_notifications(self.request.user)
        return context


# View that allows users to join or leave events
class EventMemberView(generic.View):

    @method_decorator(login_decorator)
    def post(self, request, *args, **kwargs):
        event_id = self.kwargs['event_id']
        action = request.POST['action']

        data = {}
        action_word = 'performed an invalid action on'

        try:
            event = Event.objects.get(pk=event_id)
            if action == 'join':
                action_word = 'joined'
                n_participants = len(event.participants.all())

                if n_participants >= event.max_num_participants: 
                    raise IntegrityError("max_num_participants reached")
                else:
                    join_date = timezone.now
                    Join.objects.create(user=request.user, event=event, join_date=join_date)
            elif action == 'leave':
                action_word = 'left'

                Join.objects.filter(user=request.user, event=event).delete()

            data['result'] = True
            data['participants'] = [{'name': p.first_name, 'id': p.id} for p in event.participants.all()]

            print("{} {} {}".format(request.user, action_word, event))

        except IntegrityError as e:
            print("[Warning] Exception during " + action)
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

        context['notifications'] = get_user_notifications(self.request.user)
        return context    


@method_decorator(login_decorator, name='get')
class ProfileView(generic.DetailView):
    
    template_name = 'core/pages/profile.html'
    model = User

    def get_context_data(self, **kwargs):
        user = User.objects.filter(pk=self.kwargs['pk'])[0]

        joined_events_id = list(Join.objects.filter(user=user).values_list('event', flat=True))        
        joined_events = list(Event.objects.filter(id__in=joined_events_id).exclude(event_owner=user))
        
        owned_events  = list(Event.objects.filter(event_owner=user))
                
        tags = Tag.objects.all()
        interests = user.interest_tags.all()

        context = {'user': user,
                   'joined_events': joined_events,
                   'owned_events': owned_events,
                   'tags': tags,
                   'interests': interests,
                   'notifications': get_user_notifications(self.request.user)}
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        user = User.objects.filter(pk=self.kwargs['pk'])[0]
        
        tag_ids = map(int, request.POST.getlist('selectedTags[]'))        
        tags = Tag.objects.filter(pk__in=tag_ids)
        user.interest_tags = tags
        
        data['result'] = True

        return HttpResponse(json.dumps(data))


class EventsViewSet(APIView):

    def get(self, request, *args, **kwargs):
        # Get all events that have not ended yet
        queryset = Event.objects.filter(end_date_time__gt=timezone.now())

        # Obtain the list of user scopes (interests, single tag, text filtering and date filtering)
        scopes = request.GET.getlist('scopes[]')
        print(request.GET)
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
            datetime_object = datetime.datetime.strptime(date, '%m/%d/%y')

            queryset = queryset.filter(start_date_time__gt=datetime_object)

        serializer_class = EventSerializer(queryset, many=True, context={'request': request})

        return Response(serializer_class.data) 


# Enables access to all user profiles
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Enables access to all tags
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
