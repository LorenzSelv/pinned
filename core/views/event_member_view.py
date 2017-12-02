import json

from django.views import generic
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.utils import timezone

from ..models import Event, Join
from .decorators import login_decorator

# View that allows users to join or leave events
class EventMemberView(generic.View):

    @method_decorator(login_decorator)
    def post(self, request, *args, **kwargs):
        event_id = self.kwargs['event_id']
        action = request.POST['action']

        data = {}
        action_word = 'performed an invalid action on'

        try:
            event = Event.objects.get(pk=event_id)
            if action == 'join':
                action_word = 'joined'
                n_participants = len(event.participants.all())

                if n_participants >= event.max_num_participants: 
                    raise IntegrityError("max_num_participants reached")
                else:
                    join_date = timezone.now
                    Join.objects.create(user=request.user, event=event, join_date=join_date)
            elif action == 'leave':
                action_word = 'left'

                Join.objects.filter(user=request.user, event=event).delete()

            data['result'] = True
            data['participants'] = [{'name': p.first_name, 'id': p.id} for p in event.participants.all()]

            print("{} {} {}".format(request.user, action_word, event))

        except IntegrityError as e:
            print("[Warning] Exception during " + action)
            print(str(e))
            data['result'] = False
        
        return HttpResponse(json.dumps(data))