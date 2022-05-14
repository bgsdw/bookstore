
from bookstore.app.models import Author
from bookstore.app.serializers.author_serializer import AuthorSerlializer
from rest_framework import viewsets


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerlializer
