from django import forms

class EventForm(forms.Form):
    name = forms.CharField(max_length=150)
    description = forms.CharField(max_length=1000)
    # TODO check that events can't have the same date_time AND location
    # TODO ensure that the end_date_time > start_date_time. Is it possible to do at the model level?
    start_date_time = forms.DateTimeField()
    end_date_time   = forms.DateTimeField()

    # location = forms.ForeignKey('Location', on_delete=forms.CASCADE)
    latitude = forms.DecimalField(widget=forms.HiddenInput)
    longitude = forms.DecimalField(widget=forms.HiddenInput)

    max_num_participants = forms.IntegerField()

    user = forms.IntegerField(widget=forms.HiddenInput)