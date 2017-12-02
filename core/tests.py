import random
import django
from django.test import TestCase
from django.utils import timezone
from core.models import User, Event, Location, Tag, Join, Comment, UserNotification, NotificationRating
from django.core.exceptions import ValidationError


def create_user(username):
    password = username + 'Pass'
    email    = username + '@ucsc.edu'
    phone_number = "+123456789"
    return User.objects.create(username=username,
                               password=password,
                               email=email,
                               phone_number=phone_number,
                               latitude=ILC.latitude,
                               longitude=ILC.longitude)


def get_random_color():
    v = '0123456789ABCDEF'
    return '#' + ''.join([random.choice(v) for _ in range(6)])


def create_some_tags():
    tags_name = [
        'Ping Pong', 'Football', 'Gym', 'Tennis']
    return [Tag.objects.create(name=name, color=get_random_color()) for name in tags_name]


def get_users_interested_in(tag_name):
    return Tag.objects.get(name=tag_name).interested_users.all()


def create_event(name, location, event_owner, start_date_time, end_date_time=None, max_num_participants=5):
    description = name + ' -- The best sport event on campus'
    if end_date_time is None:  # default to 90 minutes
        end_date_time = start_date_time + timezone.timedelta(minutes=90)

    return Event.objects.create(name=name,
                                description=description,
                                latitude=location.latitude,
                                longitude=location.latitude,
                                event_owner=event_owner,
                                start_date_time=start_date_time,
                                end_date_time=end_date_time,
                                max_num_participants=max_num_participants)


def get_random_latitude():
    return random.uniform(-90, +90)


def get_random_longitude():
    return random.uniform(-180, +180)


def create_location(name, latitude=None, longitude=None):
    if not latitude:
        latitude = get_random_latitude()
    if not longitude:
        longitude = get_random_longitude()
    return Location.objects.create(name=name,
                                   description=name + ' -- nice place!',
                                   latitude=latitude,
                                   longitude=longitude)
ILC = create_location('ILC')


class UserModelTests (TestCase):

    def test_insert_user(self):
        l = create_user('Lorenzo')
        a = create_user('Andrea')

        users = User.objects.all()

        self.assertEqual(len(users), 2)
        self.assertIn(l, users)
        self.assertEqual(l.username, 'Lorenzo')
        self.assertEqual(l.password, 'LorenzoPass')
        self.assertEqual(l.email, 'Lorenzo@ucsc.edu')
        self.assertIn(a, users)
        self.assertEqual(a.username, 'Andrea')
        self.assertEqual(a.password, 'AndreaPass')
        self.assertEqual(a.email, 'Andrea@ucsc.edu')

    def test_follower_following(self):
        l = create_user('Lorenzo')
        a = create_user('Andrea')
        h = create_user('Henry')

        l.followers.add(h)

        self.assertIn(h, l.followers.all())
        self.assertIn(l, h.following.all())
        # following is not a symmetrical relationship
        self.assertNotIn(l, h.followers.all())

        a.following.add(l)
        self.assertIn(l, a.following.all())
        self.assertIn(a, l.followers.all())

        self.assertEqual(len(l.followers.all()), 2)

        h.following.remove(l)
        self.assertEqual(len(h.following.all()), 0)
        self.assertEqual(len(l.followers.all()), 1)

    def test_interest_tags(self):
        tags = create_some_tags()
        l = create_user('Lorenzo')
        a = create_user('Andrea')

        l.interest_tags.add(tags[0])
        l.interest_tags.add(tags[1])

        self.assertEqual(list(l.interest_tags.all()), [tags[0], tags[1]])

        a.interest_tags.add(tags[1])
        a.interest_tags.add(tags[2])

        self.assertEqual(list(l.interest_tags.all()), [tags[0], tags[1]])
        self.assertEqual(list(a.interest_tags.all()), [tags[1], tags[2]])

        users_interested_in_0 = get_users_interested_in(tags[0].name)
        self.assertEqual(len(users_interested_in_0), 1)

        users_interested_in_1 = get_users_interested_in(tags[1].name)
        self.assertEqual(len(users_interested_in_1), 2)

    def test_unique_username(self):
        l1 = create_user('Lorenzo')
        self.assertEqual(User.objects.get(pk=1), l1)
        with self.assertRaises(django.db.utils.IntegrityError):
            l2 = create_user('Lorenzo')


class TagModelTests (TestCase):

    def test_unique_name(self):
        t1 = Tag.objects.create(name='Gym', color=get_random_color())
        with self.assertRaises(django.db.utils.IntegrityError):
            t2 = Tag.objects.create(name='Gym', color=get_random_color())

    def test_long_name(self):
        t1 = Tag.objects.create(name='abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz',
                                color=get_random_color())
        # print(t1)

    def test_color(self):
        t = Tag.objects.create(name='Gym', color=get_random_color())
        # print(t.color)


class EventModelTests (TestCase):

    def test_insert_event(self):
        lorenzo = create_user('Lorenzo')
        federico = create_user('Federico')
        pp = create_event('Ping pong', ILC, lorenzo, timezone.now(), max_num_participants=2)

        # pp.participants.add(lorenzo)  # NOT POSSIBLE: through='Join'
        Join.objects.create(user=lorenzo, event=pp)
        Join.objects.create(user=federico, event=pp)

        self.assertEqual(list(pp.participants.all()), [lorenzo, federico])

        # TODO: this operation should not be allowed since max_num_participants=2
        Join.objects.create(user=create_user('one_more'), event=pp)

    def test_join_twice(self):
        lorenzo = create_user('Lorenzo')
        federico = create_user('Federico')
        pp = create_event('Ping pong', ILC, lorenzo, timezone.now(), max_num_participants=2)

        Join.objects.create(user=lorenzo, event=pp)
        Join.objects.create(user=federico, event=pp)
        # A user cannot join twice the same event
        with self.assertRaises(django.db.utils.IntegrityError):
            Join.objects.create(user=federico, event=pp)

    def test_events_date(self):
        lorenzo = create_user('Lorenzo')
        pp = create_event('Ping pong', ILC, lorenzo, timezone.now(), max_num_participants=2)
        # Ignore milliseconds
        self.assertEqual(pp.creation_date.strftime("%Y-%m-%d %H:%M:%S"), timezone.now().strftime("%Y-%m-%d %H:%M:%S"))

    # TODO: test overlapping events at the same location, as soon as we have defined what a location is (Google MAP API)
    # TODO: test event dates with different time zones


class EventUserInteractionTests (TestCase):

    def test_delete_participant(self):
        l = create_user('Lorenzo')
        f = create_user('Federico')
        pp = create_event('Ping pong', ILC, l, timezone.now(), max_num_participants=2)

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
        pp = create_event('Ping pong', ILC, l, timezone.now(), max_num_participants=2)

        Join.objects.create(user=l, event=pp)
        Join.objects.get(id=l.id).delete()
        self.assertNotIn(l, pp.participants.all())

    def test_delete_event_owner(self):
        l = create_user('Lorenzo')
        pp = create_event('Ping pong', ILC, l, timezone.now(), max_num_participants=2)

        l.delete()
        # The event should be deleted
        with self.assertRaises(django.core.exceptions.ObjectDoesNotExist):
            event = Event.objects.get(id=pp.id)

    def test_delete_event_not_symmetric(self):
        l = create_user('Lorenzo')
        pp = create_event('Ping pong', ILC, l, timezone.now(), max_num_participants=2)

        pp.delete()
        self.assertEqual(User.objects.get(id=l.id), l)


class LocationTests (TestCase):
    dining_hall = create_location('Dining Hall', latitude=37.001435, longitude=-122.057775)

    # def test_insert_location(self):
        # print('name    ', dining_hall.name)
        # print('latitude', dining_hall.latitude)
        # print('latitude', dining_hall.longitude)

    def test_unique_name(self):
        with self.assertRaises(django.db.utils.IntegrityError):
            create_location('Dining Hall', latitude=0, longitude=0)

    def test_unique_lat_long(self):

        with self.assertRaises(django.db.utils.IntegrityError):
            create_location('Same place', latitude=37.001435, longitude=-122.057775)

    # Note: this test is not raising an exception as one would expected
    #       because of the way django handles validators
    #       See: https://docs.djangoproject.com/en/1.8/ref/validators/#how-validators-are-run
    # def test_validators_lat_long(self):
    #
    #     with self.assertRaises(django.core.exceptions.ValidationError):
    #         create_location('No-place', latitude=-99., longitude=0.)
    #
    #     with self.assertRaises(ValidationError):
    #         create_location('No-place', latitude=0., longitude=200.)
    #
    #     with self.assertRaises(ValidationError):
    #         create_location('No-place', latitude=99., longitude=-200.)


def get_user_notifications(user):
    notifications = UserNotification.objects.filter(user=user)
    return [notification.content_object for notification in notifications]


def create_notification(username, eventname, location='ILC'):
    user = create_user(username)
    event = create_event(eventname, ILC, user, timezone.now(), max_num_participants=2)

    # Create notification
    notification = NotificationRating(date=timezone.now(), event=event, user=user)
    notification.save()

    # Create link user-notification in the notification interface
    usernotif = UserNotification(content_object=notification, user=user, object_id=notification.id)
    usernotif.save()
    return usernotif


class NotificationTests (TestCase):

    def test_notification_creation(self):
        l = create_user('Lorenzo')
        pp = create_event('Ping pong', ILC, l, timezone.now(), max_num_participants=2)
        notification = NotificationRating(date=timezone.now(), event=pp, user=l)

        self.assertEqual(notification.is_read, False)
        self.assertEqual(notification.user.username, l.username)
        self.assertEqual(notification.event, pp)

    def test_notify_user(self):
        l = create_user('Lorenzo')
        pp = create_event('Ping pong', ILC, l, timezone.now(), max_num_participants=2)

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















