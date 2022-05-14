from rest_framework import serializers
from bookstore.app.models import Author

class AuthorSerlializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'