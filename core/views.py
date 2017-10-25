
from django.shortcuts import render
from django.views import generic
from rest_framework import viewsets

from .models import Event, User, Tag
from .forms import EventForm
from .serializers import EventSerializer


class MapView(generic.View):
    context = {
        "tags": Tag.objects.all(),
        "event_list": Event.objects.order_by('start_date_time')[:3]
        }

    def post(self, request):
        form = EventForm(request.POST)
        print(form.fields.keys())

        if form.is_valid():
            # e = Event(**form.cleaned_data)
            form.save()
            # form.save_m2m()
            # Event.objects.create(**form.cleaned_data)
            self.context['state'] = "saved"
        else:
            self.context['state'] = "error"
            self.context['errors'] = form.errors

        self.context['form'] = EventForm()
        return render(request, 'core/pages/map.html', context=self.context)

    def get(self, request, *args, **kwargs):
        self.context['state'] = "get"
        self.context['form'] = EventForm()
        return render(request, 'core/pages/map.html', context=self.context)


class EventsView(generic.ListView):
    template_name = 'core/pages/events.html'
    model = Event

    def get_context_data(self, **kwargs):
        context = super(EventsView, self).get_context_data(**kwargs)
        context['fields'] = Event._meta.get_fields()
        return context


class ProfileView(generic.ListView):
    template_name = 'core/pages/profile.html'
    model = User


# Enables access to all events
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
