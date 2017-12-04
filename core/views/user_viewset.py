from rest_framework import viewsets
from ..models import User
from ..serializers import UserSerializer

# Enables access to all user profiles
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer