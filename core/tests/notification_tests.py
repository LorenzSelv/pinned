import random
import django
from django.test import TestCase
from django.utils import timezone
from core.models import User, Event, UserNotification, NotificationRating

def get_random_latitude():
    return random.uniform(-90, +90)

def get_random_longitude():
    return random.uniform(-180, +180)

def create_event(name, event_owner, start_date_time, end_date_time=None, max_num_participants=5):
    description = name + ' -- The best sport event on campus'
    if end_date_time is None:  # default to 90 minutes
        end_date_time = start_date_time + timezone.timedelta(minutes=90)

    latitude = get_random_latitude()
    longitude = get_random_longitude()

    return Event.objects.create(name=name,
                                description=description,
                                latitude=latitude,
                                longitude=longitude,
                                event_owner=event_owner,
                                start_date_time=start_date_time,
                                end_date_time=end_date_time,
                                max_num_participants=max_num_participants)

def create_user(username):
    password = username + 'Pass'
    email    = username + '@ucsc.edu'
    phone_number = "+123456789"
    latitude = get_random_latitude()
    longitude = get_random_longitude()
    return User.objects.create(username=username,
                               password=password,
                               email=email,
                               phone_number=phone_number,
                               latitude=latitude,
                               longitude=longitude)

class NotificationTests (TestCase):

    def test_notification_creation(self):
        l = create_user('Lorenzo')
        pp = create_event('Ping pong', l, timezone.now(), max_num_participants=2)
        notification = NotificationRating(date=timezone.now(), event=pp, user=l)

        self.assertEqual(notification.is_read, False)
        self.assertEqual(notification.user.username, l.username)
        self.assertEqual(notification.event, pp)

    def test_notify_user(self):
        l = create_user('Lorenzo')
        pp = create_event('Ping pong', l, timezone.now(), max_num_participants=2)

        # Create notification
        notification = NotificationRating(date=timezone.now(), event=pp, user=l)
        notification.save()

        # Create link user-notification in the notification interface
        usernotif = UserNotification(content_object=notification, user=l, object_id=notification.id)
        usernotif.save()

        assert usernotif

        # Query the notification table
        notifications_of_l = UserNotification.objects.filter(user=l)

        self.assertEqual(len(notifications_of_l), 1)

        pingpong_usernotif = notifications_of_l[0]

        # Extract the RatingNotification from the UserNotificatio instance
        notification_from_query = pingpong_usernotif.content_object

        self.assertEqual(notification, notification_from_query)