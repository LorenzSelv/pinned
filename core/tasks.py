from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.models import NotificationRating, UserNotification, User, Event, NotificationEvent
from django.utils import timezone
# from math import sin, cos, radians, degrees, acos
#
#
# def distance(user, event):
#     user_lat = radians(user.latitude)
#     event_lat = radians(event.latitude)
#     longitude_diff = radians(user.longitude - event.longitude)
#     dist = (sin(user_lat) * sin(event_lat) + cos(user_lat) * cos(event_lat) * cos(longitude_diff))
#     return degrees(acos(dist)) * 69.09


@shared_task
def create_rating_notification(event_id):
    event = Event.objects.get(pk=event_id)
    # Create notification for every participant
    for user in event.participants.all():
        # Create notification
        notification = NotificationRating(date=timezone.now(), event=event, user=user)
        notification.save()

        # Create link user-notification in the notification interface
        user_notification = UserNotification(content_object=notification, user=user, object_id=notification.id)
        user_notification.save()


# @shared_task
# def create_event_notification(event_id):
#     event = Event.objects.get(pk=event_id)
#     # Create notification for every participant
#     for user in User.objects.filter(interest_tags__name__contains=event.tag.name):
#         # Check if user is less than or equal to 15 miles away from created event
#         if user.latitude is not None and user.longitude is not None and distance(user, event) <= 15:
#             print(event.name)
#             print(user.get_full_name())
#             # Create notification
#             notification = NotificationEvent(date=timezone.now(), event=event, user=user)
#             notification.save()
#
#             # Create link user-notification in the notification interface
#             user_notification = UserNotification(content_object=notification, user=user, object_id=notification.id)
#             user_notification.save()
