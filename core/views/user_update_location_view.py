from django.views import generic
from django.http import HttpResponse
from django.utils.decorators import method_decorator

from .decorators import login_decorator

@method_decorator(login_decorator, name='post')
class UserUpdateLocationView(generic.View):
    def post(self, request, *args, **kwargs):
        user = request.user
        response = None
        try:
            latitude = float(request.POST['lat'])
            longitude = float(request.POST['long'])
            user.latitude = latitude
            user.longitude = longitude
            user.save()
            response = HttpResponse('success')
            response.status_code = 200
        except ValueError:
            response = HttpResponse('failure')
            response.status_code = 400
        return response
