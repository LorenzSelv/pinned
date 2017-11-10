"""
Create a sample database for testing purposes

Usage: (run from the project base folder)
    python test_util/create_sample_db.py

Note: since it inserts entries in the database there may be UNIQUE value clashes
      SOLUTION -- run `make db` to clear the database first
"""
import os
import random
import sys
import django

# fix import problems
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# set up django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pinned.settings")
django.setup()

divider = "---------------------------------------------------------------------------"

from django.utils import timezone
from core.models import User, Event, Location, Tag, Join, Comment


def create_user(username):
    first_name = username.title()
    password = username + 'Pass'
    email    = username + '@ucsc.edu'
    phone_number = "+123456789"
    return User.objects.create(username=username,
                               password=password,
                               email=email,
                               phone_number=phone_number,
                               first_name=first_name)


def create_some_tags():
    tags_name = [
        'Ping Pong', 'Football', 'Gym', 'Tennis']
    tags_colors = [
      '62D0FF', '59DF00', 'FFA8A8', 'FFBB7D'
    ]
    return [Tag.objects.create(name=name, color=random.choice(tags_colors)) for name in tags_name]


def get_users_interested_in(tag_name):
    return Tag.objects.get(name=tag_name).interested_users.all()


def create_location(name):
    return Location.objects.create(name=name, description=name + ' description')


def create_event(name, location, event_owner, tag, start_date_time, end_date_time=None, max_num_participants=5):
    description = name + ' -- The best sport event on campus'
    if end_date_time is None:  # default to 90 minutes
        end_date_time = start_date_time + timezone.timedelta(minutes=90)

    return Event.objects.create(name=name,
                                description=description,
                                latitude=location.latitude,
                                longitude=location.latitude,
                                event_owner=event_owner,
                                tag=tag,
                                start_date_time=start_date_time,
                                end_date_time=end_date_time,
                                max_num_participants=max_num_participants)


def create_event_helper(name, location, event_owner, tag, hours_from_now):
    return create_event(name, location, event_owner, tag,
                        start_date_time=timezone.now()+timezone.timedelta(hours=hours_from_now))


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


def main():
    tags = create_some_tags()

    print(divider)
    print('Created tags')
    print('\n'.join([str(tag) for tag in tags]))

    usernames = ['Lorenzo', 'Andrea', 'Henry', 'Mattheo', 'Alessia']

    users = [create_user(username) for username in usernames]

    print(divider)
    print('Created users')
    print('\n'.join([str(user) for user in users]))

    events_data = [('Ping Pong', create_location('ILC'),   users[0], tags[0], 4),
                   ('Basket',    create_location('court'), users[1], tags[3], 2),
                   ('Gym',       create_location('opers'), users[2], tags[2], 5),
                   ('Football',  create_location('field'), users[3], tags[1], 3),
                   ('Rugby',     create_location('field2'), users[4], tags[3], 18)]

    events = [create_event_helper(*event_data) for event_data in events_data]

    print(divider)
    print('Created events')
    print('\n'.join([str(event) for event in events]))

if __name__ == '__main__':
    main()
    print(divider)
    print("Finished sample db creation")
