from bookstore.app.views.author_view import AuthorViewSet
from bookstore.app.views.book_view import BookViewSet
from bookstore.app.views.sales_view import SalesViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'author', AuthorViewSet)
router.register(r'book', BookViewSet)
router.register(r'sales', SalesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
