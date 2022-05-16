from bookstore.app.models import Book
from bookstore.app.serializers.book_serializer import (
    BookCoverUpdateSerializer, BookSerializer, BookUpdateSerializer)
from django.db.transaction import atomic
from django_filters import rest_framework as django_filters
from rest_framework import exceptions, filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        exclude = 'Cover_URL'

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(Author_ID__Is_Disabled=False).order_by('Book_ID')
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, django_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BookFilter

    @atomic
    @action(detail=False, methods=['post'])
    def add(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

    @atomic
    @action(detail=False, methods=['get'], authentication_classes=[], url_path='get(?:/(?P<pk>\d+))?')
    def get(self, request, pk=''):
        if pk:
            instance = self.get_object()
            serializer = BookSerializer(instance=instance)
            return Response(serializer.data)
            
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @atomic
    @action(detail=False, methods=['get'])
    def get_my_book(self, request): 
        queryset = self.filter_queryset(self.get_queryset()).filter(Author_ID=self.request.user.Author_ID)
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @atomic
    @action(detail=False, methods=['put'], url_path='update/(?P<pk>\d+)')
    def update_book(self, request, pk):
        try:
            instance = Book.objects.get(Book_ID=pk, Author_ID=self.request.user.Author_ID)
        except Book.DoesNotExist:
            raise exceptions.NotFound()
        serializer = BookUpdateSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()
    
    @atomic
    @action(detail=False, methods=['put'], url_path='update_cover/(?P<pk>\d+)')
    def update_cover(self, request, pk):
        try:
            instance = Book.objects.get(Book_ID=pk, Author_ID=self.request.user.Author_ID)
        except Book.DoesNotExist:
            raise exceptions.NotFound()
        serializer = BookCoverUpdateSerializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

    @atomic
    @action(detail=False, methods=['put'], url_path='delete/(?P<pk>\d+)')
    def delete(self, request, pk):
        try:
            instance = Book.objects.get(Book_ID=pk, Author_ID=self.request.user.Author_ID)
        except Book.DoesNotExist:
            raise exceptions.NotFound()
        instance.delete()
        return Response()
