from django import forms
from .models import Event
from django.core.exceptions import ValidationError
from django.utils import timezone


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['participants']
        widgets = {'latitude': forms.HiddenInput(),
                   'longitude': forms.HiddenInput(),
                   'description': forms.Textarea(),
                   'start_date_time': forms.TextInput(attrs={'class': 'date-time-picker'}),
                   'end_date_time': forms.TextInput(attrs={'class': 'date-time-picker'}),
                   'tags': forms.SelectMultiple(attrs={'class': 'select-multiple'}),
                   # TODO hidden input ?
                   'event_owner': forms.HiddenInput()
                   }

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        start_date_time = cleaned_data.get("start_date_time")
        end_date_time = cleaned_data.get("end_date_time")

        if start_date_time and end_date_time:
            if start_date_time < timezone.now():
                raise ValidationError("Start time cannot be prior to the current time!")

            if end_date_time < start_date_time:
                raise ValidationError("End time cannot be earlier than start time!")
        else:
            raise ValidationError("Missing date and time for the event!")
        return cleaned_data
