from bookstore.app.authentications import get_token_header
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
        # hash the password
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

        # set the access token payload
        payload = {
            'Author_ID': author.Author_ID,
            'Name': author.Name,
            'Pen_Name': author.Pen_Name,
            'Email': author.Email,
            'token_type': 'access',
            'exp': timezone.now() + timedelta(minutes=15),
        }
        # create the access token
        access_token = JWTService.encode_token(payload)
        
        # set the refresh token payload
        payload = {
            'Author_ID': author.Author_ID,
            'Name': author.Name,
            'Pen_Name': author.Pen_Name,
            'Email': author.Email,
            'token_type': 'refresh',
            'exp': timezone.now() + timedelta(days=1),
        }
        # create the refresh token
        refresh_token = JWTService.encode_token(payload)

        # return the access token and refresh token
        return {
            'Access_Token': access_token,
            'Refresh_Token': refresh_token,
        }


class ForgotPasswordSerializer(serializers.Serializer):
    Email = serializers.EmailField()

    def forgot_password(self, validated_data):
        # try to find the user, if no user is found, raise an error
        try:
            author = Author.objects.get(Email=validated_data['Email'])
        except Author.DoesNotExist:
            raise exceptions.AuthenticationFailed('Author not found with this credential.')

        new_password = 'i0sI988as'
        # update the author password
        author.Password = make_password(new_password)
        author.save()
        # return the new password
        return {
            'New_Password': new_password
        }

class ChangePasswordSerializer(serializers.Serializer):
    Old_Password = serializers.CharField()
    New_Password = serializers.CharField()

    def change_password(self, validated_data):
        # try to find the user, if no user is found, raise an error
        try:
            author = Author.objects.get(Email=self.context['request'].user.Email)
        except Author.DoesNotExist:
            raise exceptions.AuthenticationFailed('Author not found with this credential.')

        # check the password
        if not check_password(validated_data['Old_Password'], author.Password):
            raise exceptions.AuthenticationFailed('Wrong credential.')

        # update the author password
        author.Password = make_password(validated_data['New_Password'])
        author.save()

class RefreshTokenSerializer(serializers.Serializer):
    Refresh_Token = serializers.CharField()

    def refresh_token(self, validated_data):
        decoded_token = JWTService.decode_token(validated_data['Refresh_Token'], False)

        if decoded_token['token_type'] != 'refresh':
            raise exceptions.AuthenticationFailed('Refresh token invalid.')
        
        # try to find the user, if no user is found, raise an error
        try:
            author = Author.objects.get(Email=decoded_token['Email'])
        except Author.DoesNotExist:
            raise exceptions.AuthenticationFailed('Author not found with this credential.')

        # set the access token payload
        payload = {
            'Author_ID': author.Author_ID,
            'Name': author.Name,
            'Pen_Name': author.Pen_Name,
            'Email': author.Email,
            'token_type': 'access',
            'exp': timezone.now() + timedelta(minutes=15),
        }
        # create the access token
        access_token = JWTService.encode_token(payload)
        
        # set the refresh token payload
        payload = {
            'Author_ID': author.Author_ID,
            'Name': author.Name,
            'Pen_Name': author.Pen_Name,
            'Email': author.Email,
            'token_type': 'refresh',
            'exp': timezone.now() + timedelta(days=1),
        }
        # create the refresh token
        refresh_token = JWTService.encode_token(payload)

        # return the access token and refresh token
        return {
            'Access_Token': access_token,
            'Refresh_Token': refresh_token,
        }
