from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.models import NotificationRating, UserNotification, User, Event
from django.utils import timezone


@shared_task
def create_notification(event_id):
    event = Event.objects.get(pk=event_id)
    # Create notification for every participant
    for user in event.participants.all():
        # Create notification
        notification = NotificationRating(date=timezone.now(), event=event, user=user)
        notification.save()

        # Create link user-notification in the notification interface
        user_notification = UserNotification(content_object=notification, user=user, object_id=notification.id)
        user_notification.save()
