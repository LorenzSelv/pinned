from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from colorful.fields import RGBColorField
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# TODO text field vs char field

class User (AbstractUser):
    # Add a check to ensure max_length isn't exceeded? (for all classes)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)  
    email    = models.EmailField()
    picture = models.CharField(max_length=255, default='')

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)  # validators should be a list

    # TODO rating

    interest_tags = models.ManyToManyField('Tag', related_name='interested_users')

    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.first_name


# class Rating (models.Model):
#     pass


def validate_latitude(latitude):
    if not -90 <= latitude <= +90:
        raise ValidationError('%(latitude) is not in the range [-90, +90]', params={'value': latitude})


def validate_longitude(longitude):
    if not -180 <= longitude <= +180:
        raise ValidationError('%(longitude) is not in the range [-180, +180]', params={'value': longitude})


class Event (models.Model):
    name        = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    # TODO check that events can't have the same date_time AND location
    start_date_time = models.DateTimeField()
    end_date_time   = models.DateTimeField()

    # location = models.ForeignKey('Location', on_delete=models.CASCADE)
    latitude = models.DecimalField('Latitude', max_digits=10, decimal_places=8,
                                   blank=False, validators=[validate_latitude])
    longitude = models.DecimalField('Longitude', max_digits=11, decimal_places=8,
                                    blank=False, validators=[validate_longitude])

    # TODO event type: private, public --> hierarchy in django

    tag = models.ForeignKey('Tag', related_name='events', blank=True, null=True, on_delete=models.CASCADE)
    event_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    creation_date = models.DateTimeField(auto_now_add=True)

    participants = models.ManyToManyField('User', through='Join', blank=True)
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
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=1000)
    # location coordinates w/ google API
    # https://stackoverflow.com/questions/6345601/django-and-keeping-coordinates

    latitude  = models.DecimalField('Latitude',  max_digits=10, decimal_places=8,
                                    blank=False, validators=[validate_latitude])
    longitude = models.DecimalField('Longitude', max_digits=11, decimal_places=8,
                                    blank=False, validators=[validate_longitude])

    class Meta:
        # avoid inserting the same location multiple times
        unique_together = ('latitude', 'longitude')

    # TODO location images
    # TODO link google reviews?

    def __str__(self):
        return self.name


class Tag (models.Model):
    name = models.CharField(max_length=20, unique=True)
    color = RGBColorField()

    def __str__(self):
        return self.name

    def html(self):
        return '<span class="badge badge-secondary" style="background-color:#' + \
                str(self.color) + '">' + self.name + '</span>'


class Comment (models.Model):
    user = models.ForeignKey('User')
    event = models.ForeignKey('Event')
    content = models.CharField(max_length=1000)

    def __str__(self):
        return '[ ' + self.user.username + ' -- ' + self.event.name + ' ]  ' + self.content


class Notification (models.Model):
    """
    Abstract base class for notifications
    """
    # User who gets the notification
    user = models.ForeignKey('User')
    # Date when the notification was received
    date = models.DateTimeField(auto_now_add=True)
    # Whether or not the notification has been read
    is_read = models.BooleanField(default=False)
    # String representation of the type
    type = models.CharField(max_length=15, default='Base')

    class Meta:
        abstract = True

    def __str__(self):
        read = (" NOT " if not self.is_read else " ") + "READ"
        return self.type + " " + str(self.date) + " -- " + read


class NotificationRating (Notification):
    """
    A notification the user gets after each event.
    Should appear along with a link to a form for rating the participants.
    """
    event = models.ForeignKey('Event')
    type = 'Rating'

    def __str__(self):
        return self.type + " " + self.event.name + " " + Notification.__str__(self)


class UserNotification (models.Model):
    """
    Map each notification to its user.
    """

    user = models.ForeignKey('User')
    # Polymorphic reference to a Notification
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.CharField(max_length=50, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

















