from bookstore.app.models import Book
from bookstore.app.serializers.book_serializer import BookSerializer
from rest_framework import viewsets


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
