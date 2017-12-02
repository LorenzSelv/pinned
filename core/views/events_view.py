from django.views import generic
from django.utils.decorators import method_decorator

from ..models import Event, Join

from .decorators import login_decorator
from .utils import get_user_notifications

@method_decorator(login_decorator, name='get')
class EventsView(generic.ListView):
    template_name = 'core/pages/events.html'
    model = Event

    def get_context_data(self, **kwargs):  # Add field names to the context
        context = super(EventsView, self).get_context_data(**kwargs)
        joined_events = {}
        user_id = self.request.user.id
        for event in context['event_list']:
            exists = Join.objects.filter(user__pk=user_id, event__pk=event.id).exists()
            if exists:
                joined_events[event.id] = True
        context['fields'] = Event._meta.get_fields()
        context['joined_events'] = joined_events

        context['notifications'] = get_user_notifications(self.request.user)
        return context