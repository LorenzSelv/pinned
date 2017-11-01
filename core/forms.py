from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['participants']
        widgets = {'latitude': forms.HiddenInput(),
                   'longitude': forms.HiddenInput(),
                   'description': forms.Textarea(),
                   'start_date_time': forms.TextInput(attrs={'class': 'date-time-picker'}),
                   'end_date_time': forms.TextInput(attrs={'class': 'date-time-picker'}),
                   'tags': forms.SelectMultiple(attrs={'class': 'select-multiple'})}
