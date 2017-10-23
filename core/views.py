
from django.shortcuts import render
from django.views import generic

from .models import Event, User, Tag
from .forms import EventForm
# class MapView(generic.ListView):
#     template_name = 'core/map.html'
#
#     def get_queryset(self):
#         return Event.objects.order_by('-start_date_time').reverse()
# =======


class MapView(generic.View):
    context = {
        "tags": Tag.objects.all(),
        "event_list": Event.objects.order_by('-start_date_time').reverse()
        }

    def post(self, request):
        form = EventForm(request.POST)

        if(form.is_valid()):
            form.cleaned_data['event_owner'] = User.objects.get(pk=form.cleaned_data["user"])
            form.cleaned_data.pop("user", None)
            e = Event(**form.cleaned_data)
            e.save()
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
