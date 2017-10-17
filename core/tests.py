import django
from django.test import TestCase
from core.models import User, Event, Location, Tag, Join, Comment


def create_user(username):
    password = username + 'Pass'
    email    = username + '@ucsc.edu'
    phone_number = "+123456789"
    return User.objects.create(username=username,
                               password=password,
                               email=email,
                               phone_number=phone_number)


def create_some_tags():
    tags_name = [
        'Ping Pong', 'Football', 'Gym', 'Tennis']
    return [Tag.objects.create(name=name) for name in tags_name]


def get_users_interested_in(tag_name):
    return Tag.objects.get(name=tag_name).interested_users.all()


def create_event(name, location, event_owner, max_num_participants=5):
    description = name + ' -- The best sport event on campus'
    return Event.objects.create(name=name,
                                description=description,
                                location=location,
                                event_owner=event_owner,
                                max_num_participants=max_num_participants)


class UserModelTests (TestCase):

    def test_insert_user(self):
        l = create_user('Lorenzo')
        a = create_user('Andrea')

        users = User.objects.all()

        self.assertIn(l, users)
        self.assertIn(a, users)
        self.assertEqual(len(users), 2)
        self.assertEqual(l.username, 'Lorenzo')
        self.assertEqual(a.password, 'AndreaPass')

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

    def test_unique_username(self):
        with self.assertRaises(django.db.utils.IntegrityError):
            l1 = Tag.objects.create(name='Gym')
            l2 = Tag.objects.create(name='Gym')


class EventModelTests (TestCase):

    def test_insert_events(self):
        lorenzo = create_user('Lorenzo')
        federico = create_user('Federico')

        ILC = Location.objects.create(name='ILC')
        pp = create_event('Ping pong', ILC, lorenzo, max_num_participants=2)

        # pp.participants.add(lorenzo)  # NOT POSSIBLE: through='Join'
        Join.objects.create(user=lorenzo, event=pp)
        Join.objects.create(user=federico, event=pp)

        self.assertEqual(list(pp.participants.all()), [lorenzo, federico])

        # TODO: this operation should not be allowed since max_num_participants=2
        Join.objects.create(user=create_user('one_more'), event=pp)

    def test_join_twice(self):
        lorenzo = create_user('Lorenzo')
        federico = create_user('Federico')

        ILC = Location.objects.create(name='ILC')
        pp = create_event('Ping pong', ILC, lorenzo, max_num_participants=2)

        Join.objects.create(user=lorenzo, event=pp)
        Join.objects.create(user=federico, event=pp)
        # A user cannot join twice the same event
        with self.assertRaises(django.db.utils.IntegrityError):
            Join.objects.create(user=federico, event=pp)

    def test_filter_events_date(self):
        pass


class EventUserInteractionTests (TestCase):

    def test_delete_participant(self):
        pass

    def test_delete_event_owner(self):
        pass









