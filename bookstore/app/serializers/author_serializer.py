from bookstore.app.models import Author
from rest_framework import serializers


class AuthorSerlializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
