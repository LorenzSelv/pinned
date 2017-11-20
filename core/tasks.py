from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.models import NotificationRating, UserNotification, User, Event
from django.utils import timezone


@shared_task
def create_notification(user_id, event_id):
    user = User.objects.get(pk=user_id)
    event = Event.objects.get(pk=event_id)
    # Create notification
    notification = NotificationRating(date=timezone.now(), event=event, user=user)
    notification.save()

    # Create link user-notification in the notification interface
    user_notification = UserNotification(content_object=notification, user=user, object_id=notification.id)
    user_notification.save()
    return user_notification.content_object

