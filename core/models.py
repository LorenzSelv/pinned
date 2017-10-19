from django.db import models
from django import forms
from django.core.validators import RegexValidator, MinValueValidator


# TODO text field vs char field

class User (models.Model):
    # Add a check to ensure max_length isn't exceeded? (for all classes)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)  # (widget=forms.PasswordInput)
    email    = models.EmailField()

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)  # validators should be a list

    # TODO rating

    interest_tags = models.ManyToManyField('Tag', related_name='interested_users')

    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')

    def __str__(self):
        return self.username


# class Rating (models.Model):
#     pass


class Event (models.Model):
    name        = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    # TODO check that events can't have the same date_time AND location
    # TODO ensure that the end_date_time > start_date_time. Is it possible to do at the model level?
    start_date_time = models.DateTimeField()
    end_date_time   = models.DateTimeField()
    location    = models.ForeignKey('Location', on_delete=models.CASCADE)

    # TODO event type: private, public --> hierarchy in django
    tags = models.ManyToManyField('Tag', related_name='events')

    event_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    creation_date = models.DateTimeField(auto_now_add=True)

    participants = models.ManyToManyField('User', through='Join')
    max_num_participants = models.IntegerField(
        validators=[MinValueValidator(2, message='At least two people are allowed to join')])

    def __str__(self):
        return self.name + ' - ' + self.event_owner.username


class Join (models.Model):
    # Note: an explicit join model allows to store detailed
    #       information such as join_date. They may be useful.
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return self.user.username + ' - ' + self.event.name


class Location (models.Model):
    # Note: change the field according to Google maps API specs
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=1000)
    # TODO location coordinates w/ google API
    # TODO location images
    # TODO link google reviews?

    def __str__(self):
        return self.name


class Tag (models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Comment (models.Model):
    user = models.ForeignKey('User')
    event = models.ForeignKey('Event')
    content = models.CharField(max_length=1000)

    def __str__(self):
        return '[ ' + self.user.username + ' -- ' + self.event.name + ' ]  ' + self.content
