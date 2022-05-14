from rest_framework import routers
from django.urls import path, include

from bookstore.app.views.authot_view import AuthorViewSet

router = routers.DefaultRouter()
router.register(r'author', AuthorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]