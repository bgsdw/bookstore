from bookstore.app.models import Book
from bookstore.app.serializers.book_serializer import BookSerializer
from django.db.transaction import atomic
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]

    @atomic
    @action(detail=False, methods=['post'])
    def add(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response()

    @atomic
    @action(detail=False, methods=['get'], authentication_classes=[])
    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'List_Data': serializer.data})
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({'List_Data': serializer.data})
