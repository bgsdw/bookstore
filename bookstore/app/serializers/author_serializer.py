from bookstore.app.models import Author
from bookstore.app.services.jwt_service import JWTService
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from rest_framework import exceptions, serializers
from datetime import timedelta


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
        # try to find the user, if no user is found, raise an error
        try:
            author = Author.objects.get(Email=validated_data['Email'])
        except Author.DoesNotExist:
            raise exceptions.AuthenticationFailed('Author not found with this credential.')

        # check the password
        if not check_password(validated_data['Password'], author.Password):
            raise exceptions.AuthenticationFailed('Wrong credential.')

        payload = {
            'Author_ID': author.Author_ID,
            'Name': author.Name,
            'Pen_Name': author.Pen_Name,
            'Email': author.Email,
            'token_type': 'access',
            'exp': timezone.now() + timedelta(minutes=15),
        }
        access_token = JWTService.generate_token(payload)
        
        payload = {
            'Author_ID': author.Author_ID,
            'Name': author.Name,
            'Pen_Name': author.Pen_Name,
            'Email': author.Email,
            'token_type': 'refresh',
            'exp': timezone.now() + timedelta(days=1),
        }
        refresh_token = JWTService.generate_token(payload)

        return {
            'Access_Token': access_token,
            'Refresh_Token': refresh_token,
        }
