import random
import django
from django.test import TestCase
from django.utils import timezone
from core.models import User, Event, Location, Tag, Join, Comment, UserNotification, NotificationRating
from django.core.exceptions import ValidationError

from .event_model_tests import *
from .user_model_tests import *
from .tag_model_tests import *
from .event_user_interaction_tests import *
from .notification_tests import *
from .profile_view_tests import *
from .events_view_tests import *
from .event_view_tests import *
#from .map_view_tests import *

def get_user_notifications(user):
    notifications = UserNotification.objects.filter(user=user)
    return [notification.content_object for notification in notifications]


def create_notification(username, eventname, location='ILC'):
    user = create_user(username)
    event = create_event(eventname, user, timezone.now(), max_num_participants=2)

    # Create notification
    notification = NotificationRating(date=timezone.now(), event=event, user=user)
    notification.save()

    # Create link user-notification in the notification interface
    usernotif = UserNotification(content_object=notification, user=user, object_id=notification.id)
    usernotif.save()
    return usernotif





