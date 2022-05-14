
from rest_framework import viewsets
from bookstore.app.models import Author
from bookstore.app.serializers.author_serializer import AuthorSerlializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerlializer