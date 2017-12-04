import random
import django
from django.test import TestCase
from core.models import Tag

def get_random_color():
    v = '0123456789ABCDEF'
    return '#' + ''.join([random.choice(v) for _ in range(6)])

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