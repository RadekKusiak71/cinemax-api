from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all(), lookup='iexact', message="A user with that email already exists.")])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'password_confirmation', 'date_joined',]
        read_only_fields = ['id', 'date_joined',]

    def validate(self, attrs: dict) -> dict:
        if attrs.get('password') != attrs.get('password_confirmation'):
            raise serializers.ValidationError({"password_confirmation": "Password fields didn't match."})
        return attrs

    def create(self, validated_data: dict) -> User:
        validated_data.pop('password_confirmation', None)
        user: User = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user