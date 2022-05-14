from bookstore.app.models import Author
from bookstore.app.serializers.author_serializer import (AuthorSerlializer, ChangePasswordSerializer, ForgotPasswordSerializer,
                                                         LoginSerializer, RefreshTokenSerializer)
from django.db.transaction import atomic
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerlializer

    def get_object(self):
        return self.request.user

    def update(self, request, pk=None):
        instance = self.get_object()
        serializer = AuthorSerlializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

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
        token = serializer.authenticate(serializer.data)
        return Response(token)
        
    @atomic
    @action(detail=False, methods=['post'])
    def logout(self, request):
        return Response()

    @atomic
    @action(detail=False, methods=['post'], authentication_classes=[])
    def forgot_password(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.forgot_password(serializer.data)
        return Response(new_password)

    @atomic
    @action(detail=False, methods=['put'])
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.change_password(serializer.data)
        return Response()

    @atomic
    @action(detail=False, methods=['post'], authentication_classes=[])
    def refresh_token(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.refresh_token(serializer.data)
        return Response(token)

    @atomic
    @action(detail=False, methods=['delete'])
    def delete(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.delete_author(serializer.data, self.request.user)
        return Response()

    @atomic
    @action(detail=False, methods=['get'])
    def get_my_profile(self, request):
        instance = self.get_object()
        serializer = AuthorSerlializer(instance=instance)
        return Response(serializer.data)
