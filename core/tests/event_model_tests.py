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

class EventModelTests (TestCase):

    def test_insert_event(self):
        lorenzo = create_user('Lorenzo')
        federico = create_user('Federico')
        pp = create_event('Ping pong', lorenzo, timezone.now(), max_num_participants=2)

        # pp.participants.add(lorenzo)  # NOT POSSIBLE: through='Join'
        Join.objects.create(user=lorenzo, event=pp)
        Join.objects.create(user=federico, event=pp)

        self.assertEqual(list(pp.participants.all()), [lorenzo, federico])

        # TODO: this operation should not be allowed since max_num_participants=2
        Join.objects.create(user=create_user('one_more'), event=pp)

    def test_join_twice(self):
        lorenzo = create_user('Lorenzo')
        federico = create_user('Federico')
        pp = create_event('Ping pong', lorenzo, timezone.now(), max_num_participants=2)

        Join.objects.create(user=lorenzo, event=pp)
        Join.objects.create(user=federico, event=pp)
        # A user cannot join twice the same event
        with self.assertRaises(django.db.utils.IntegrityError):
            Join.objects.create(user=federico, event=pp)

    def test_events_date(self):
        lorenzo = create_user('Lorenzo')
        pp = create_event('Ping pong', lorenzo, timezone.now(), max_num_participants=2)
        # Ignore milliseconds
        self.assertEqual(pp.creation_date.strftime("%Y-%m-%d %H:%M:%S"), timezone.now().strftime("%Y-%m-%d %H:%M:%S"))

    # TODO: test overlapping events at the same location, as soon as we have defined what a location is (Google MAP API)
    # TODO: test event dates with different time zones