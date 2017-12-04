import random
import django
from django.test import TestCase
from django.utils import timezone
from core.models import User, Event, Join

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

class EventUserInteractionTests (TestCase):

    def test_delete_participant(self):
        l = create_user('Lorenzo')
        f = create_user('Federico')
        pp = create_event('Ping pong', l, timezone.now(), max_num_participants=2)

        Join.objects.create(user=l, event=pp)
        Join.objects.create(user=f, event=pp)
        self.assertIn(f, pp.participants.all())
        Join.objects.get(id=f.id).delete()
        self.assertNotIn(f, pp.participants.all())
        # Lorenzo is still a participant
        self.assertIn(l, pp.participants.all())

    # Should this work? Discuss..
    def test_delete_event_owner_as_participant(self):
        l = create_user('Lorenzo')
        pp = create_event('Ping pong', l, timezone.now(), max_num_participants=2)

        Join.objects.create(user=l, event=pp)
        Join.objects.get(id=l.id).delete()
        self.assertNotIn(l, pp.participants.all())

    def test_delete_event_owner(self):
        l = create_user('Lorenzo')
        pp = create_event('Ping pong', l, timezone.now(), max_num_participants=2)

        l.delete()
        # The event should be deleted
        with self.assertRaises(django.core.exceptions.ObjectDoesNotExist):
            event = Event.objects.get(id=pp.id)

    def test_delete_event_not_symmetric(self):
        l = create_user('Lorenzo')
        pp = create_event('Ping pong', l, timezone.now(), max_num_participants=2)

        pp.delete()
        self.assertEqual(User.objects.get(id=l.id), l)