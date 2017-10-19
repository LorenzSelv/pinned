"""
Create a sample database for testing purposes

Usage: (run from the project base folder)
    python test_util/create_sample_db.py

Note: since it inserts entries in the database there may be UNIQUE value clashes
      SOLUTION -- run `make db` to clear the database first
"""
import os
import sys
import django

# fix import problems
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# set up django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pinned.settings")
django.setup()

from django.utils import timezone
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


def create_location(name):
    return Location.objects.create(name=name, description=name + ' description')


def create_event(name, location, event_owner, start_date_time, end_date_time=None, max_num_participants=5):
    description = name + ' -- The best sport event on campus'
    if end_date_time is None:  # default to 90 minutes
        end_date_time = start_date_time + timezone.timedelta(minutes=90)

    return Event.objects.create(name=name,
                                description=description,
                                location=location,
                                event_owner=event_owner,
                                start_date_time=start_date_time,
                                end_date_time=end_date_time,
                                max_num_participants=max_num_participants)


def create_event_helper(name, location, event_owner, hours_from_now):
    return create_event(name, location, event_owner,
                        start_date_time=timezone.now()+timezone.timedelta(hours=hours_from_now))


def main():
    usernames = ['Lorenzo', 'Andrea', 'Henry', 'Mattheo', 'Alessia']

    users = [create_user(username) for username in usernames]

    events_data = [('Ping Pong', create_location('ILC'),   users[0], 4),
                   ('Basket',    create_location('court'), users[1], 2),
                   ('Gym',       create_location('opers'), users[2], 5),
                   ('Football',  create_location('field'), users[3], 3),
                   ('Rugby',     create_location('field2'), users[4], 18)]

    events = [create_event_helper(*event_data) for event_data in events_data]

    print('Created users')
    print('\n'.join([str(user) for user in users]))

    print('Created events')
    print('\n'.join([str(event) for event in events]))


if __name__ == '__main__':
    main()
