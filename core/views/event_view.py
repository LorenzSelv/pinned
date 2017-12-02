from django.views import generic
from django.utils.decorators import method_decorator

from ..models import Event, Join

from .decorators import login_decorator
from .utils import get_user_notifications

@method_decorator(login_decorator, name='get')
class EventView(generic.DetailView):
    template_name = 'core/pages/event.html'
    model = Event

    def get_context_data(self, **kwargs):
        user_id = self.request.user.id
        context = super(EventView, self).get_context_data(**kwargs)
        context['joined'] = Join.objects.filter(user__pk=user_id, event__pk=self.kwargs['pk']).exists()

        context['notifications'] = get_user_notifications(self.request.user)
        return context    