from django.shortcuts import redirect

from .user_viewset import *
from .tag_viewset import *
from .event_viewset import *

from .event_view import *
from .map_view import *
from .events_view import *
from .profile_view import *

from .event_member_view import *
from .tag_create_view import *

def login(request):
    if request.user.is_authenticated():
        return redirect('map/')
    return redirect('/login/auth0')