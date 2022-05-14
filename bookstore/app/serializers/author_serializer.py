from bookstore.app.models import Author
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class AuthorSerlializer(serializers.ModelSerializer):
    Password = serializers.CharField(write_only=True)

    class Meta:
        model = Author
        fields = '__all__'

    def create(self, validated_data):
        validated_data['Password'] = make_password(validated_data['Password'])
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    Email = serializers.EmailField()
    Password = serializers.CharField()

    def authenticate(self, validated_data):
        pass