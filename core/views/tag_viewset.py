from rest_framework import viewsets
from ..models import Tag
from ..serializers import TagSerializer

# Enables access to all tags
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
