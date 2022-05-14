from bookstore.app.models import Author
from bookstore.app.serializers.author_serializer import AuthorSerlializer, LoginSerializer
from django.db.transaction import atomic
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerlializer

    @atomic
    @action(detail=False, methods=['post'], authentication_classes=[])
    def register(self, request):
        serializer = AuthorSerlializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()


    @atomic
    @action(detail=False, methods=['post'], authentication_classes=[])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.authenticate(serializer.data)
        return Response()
        
