import json
from django.views import generic
from django.utils.decorators import method_decorator
from django.http import HttpResponse

from ..models import User, Join, Event, Tag

from .decorators import login_decorator
from .utils import get_user_notifications

@method_decorator(login_decorator, name='get')
class ProfileView(generic.DetailView):
    
    template_name = 'core/pages/profile.html'
    model = User

    def get_context_data(self, **kwargs):
        user = User.objects.filter(pk=self.kwargs['pk'])[0]

        joined_events_id = list(Join.objects.filter(user=user).values_list('event', flat=True))        
        joined_events = list(Event.objects.filter(id__in=joined_events_id).exclude(event_owner=user))
        
        owned_events  = list(Event.objects.filter(event_owner=user))
                
        tags = Tag.objects.order_by('name') 
        interests = user.interest_tags.all()

        context = {'user': user,
                   'joined_events': joined_events,
                   'owned_events': owned_events,
                   'tags': tags,
                   'interests': interests,
                   'notifications': get_user_notifications(self.request.user),
                   'same_user': user == self.request.user}
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        user = User.objects.filter(pk=self.kwargs['pk'])[0]
        if user != request.user:
          data['result'] = False
        else:
          tag_ids = map(int, request.POST.getlist('selectedTags[]'))        
          tags = Tag.objects.filter(pk__in=tag_ids)
          user.interest_tags = tags
          
          data['result'] = True

        return HttpResponse(json.dumps(data))
