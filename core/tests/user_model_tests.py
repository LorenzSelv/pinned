import random
import django
from django.test import TestCase
from django.utils import timezone
from core.models import User, Event, Tag

def get_random_color():
    v = '0123456789ABCDEF'
    return '#' + ''.join([random.choice(v) for _ in range(6)])

def get_random_latitude():
    return random.uniform(-90, +90)

def get_random_longitude():
    return random.uniform(-180, +180)

def create_some_tags():
    tags_name = [
        'Ping Pong', 'Football', 'Gym', 'Tennis']
    return [Tag.objects.create(name=name, color=get_random_color()) for name in tags_name]

def get_users_interested_in(tag_name):
    return Tag.objects.get(name=tag_name).interested_users.all()

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