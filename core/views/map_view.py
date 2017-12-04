from math import sin, cos, radians, degrees, acos 

from django.views import generic
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator

from ..models import Event, User, NotificationEvent, UserNotification
from ..forms import EventForm

from .decorators import login_decorator
from .utils import get_user_notifications


class MapView(generic.View):

    @staticmethod
    def get_default_context():
        now = timezone.now()
        context = {
            "event_list": Event.objects.filter(end_date_time__gt=now, start_date_time__gt=now)
                                       .order_by('start_date_time')[:3]
            }
        return context

    @method_decorator(login_decorator)
    def post(self, request):

        self.context = MapView.get_default_context()

        def create_event_notification(event):

            def distance(user, event):
                user_lat = radians(user.latitude)
                event_lat = radians(event.latitude)
                longitude_diff = radians(user.longitude - event.longitude)
                dist = (sin(user_lat) * sin(event_lat) + cos(user_lat) * cos(event_lat) * cos(longitude_diff))
                return degrees(acos(dist)) * 69.09

            # Create notification for every participant
            if event.tag is not None:
                for user in User.objects.filter(interest_tags__name__contains=event.tag.name).exclude(pk=request.user.pk):
                    # Check if user is less than or equal to 15 miles away from created event
                    if user.latitude is not None and user.longitude is not None and distance(user, event) <= 15:
                        # Create notification
                        notification = NotificationEvent(date=timezone.now(), event=event, user=user)
                        notification.save()

                        # Create link user-notification in the notification interface
                        user_notification = UserNotification(content_object=notification, user=user,
                                                             object_id=notification.id)
                        user_notification.save()

        try:
            form_temp = EventForm(request.POST)
            form = form_temp.save(commit=False)
            form.event_owner = request.user
            form.save()
            form_temp.save_m2m() # Needed for saving tags, added by using "commit=False"
            self.context['state'] = "saved"
            create_event_notification(form)
            self.context['notifications'] = get_user_notifications(request.user)
        except ValueError as e:
            self.context['state'] = "error"
            self.context['errors'] = form_temp.errors
            self.context['other_errors'] = form_temp.non_field_errors()
            print(e)

        self.context['form'] = EventForm()
        return render(request, 'core/pages/map.html', context=self.context)

    def get(self, request, *args, **kwargs):

        self.context = MapView.get_default_context()
        self.context['state'] = "get"
        if request.user.is_authenticated():
            self.context['form'] = EventForm()
            user_id = request.user.id
            user = User.objects.get(pk=user_id)
            tags = user.interest_tags.all()
            self.context['tags'] = tags
            self.context['notifications'] = get_user_notifications(user)
            self.context.pop('not_logged_in', None)
        else:
            self.context['not_logged_in'] = True
        return render(request, 'core/pages/map.html', context=self.context)
