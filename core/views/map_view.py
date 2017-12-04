from django.views import generic
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator

from ..models import Event, User
from ..forms import EventForm

from .decorators import login_decorator
from .utils import get_user_notifications

class MapView(generic.View):
    now = timezone.now()
    context = {
        "event_list": Event.objects.filter(end_date_time__gt=now, start_date_time__gt=now).filter()
                                   .order_by('start_date_time')[:3]
        }

    @method_decorator(login_decorator)
    def post(self, request):

        try:
            form_temp = EventForm(request.POST)
            form = form_temp.save(commit=False)
            form.event_owner = request.user
            form.save()
            form_temp.save_m2m() # Needed for saving tags, added by using "commit=False"
            self.context['state'] = "saved"
        except ValueError as e:
            self.context['state'] = "error"
            self.context['errors'] = form_temp.errors
            self.context['other_errors'] = form_temp.non_field_errors()
            print(e)

        self.context['form'] = EventForm()
        return render(request, 'core/pages/map.html', context=self.context)

    def get(self, request, *args, **kwargs):
        self.context['state'] = "get"
        if request.user.is_authenticated():
            self.context['form'] = EventForm()
            user_id = request.user.id
            user = User.objects.get(pk=user_id)
            tags = user.interest_tags.all()
            self.context['tags'] = tags
            self.context['notifications'] = get_user_notifications(user)
            self.context.pop('not_logged_in', None)
        else:
            self.context['not_logged_in'] = True
        return render(request, 'core/pages/map.html', context=self.context)
