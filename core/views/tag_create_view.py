import random
import string
import json

from django.views import generic
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.utils.decorators import method_decorator

from ..models import Tag

from .decorators import login_decorator


@method_decorator(login_decorator, name='post')
class TagCreateView(generic.View):

    def post(self, request, *args, **kwargs):
        tag_name = request.POST['tagName']
        color = ''.join(random.choice(string.hexdigits) for _ in range(6))
        try:
            tag = Tag.objects.create(name=tag_name, color=color)
        except IntegrityError:
            tag = {'id': -1}

        return HttpResponse(json.dumps({'id': tag.id}))
