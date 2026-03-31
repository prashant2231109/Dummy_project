from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction

from subscriber.models import Subscriber, Company




class SignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all()
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "email",
            "company",
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

 
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    @transaction.atomic
    def create(self, validated_data):
        company = validated_data.pop("company")
        validated_data.pop("confirm_password")

        user = User.objects.create_user(**validated_data)

        Subscriber.objects.create(
            user=user,
            company=company
        )

        return user





class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

      
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username or password")

        if not user.is_active:
            raise serializers.ValidationError("User is inactive")

        data["user"] = user
        return data

