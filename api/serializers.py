from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import User, Post


class UserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False)
    username = serializers.CharField(
        required=True,
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    email = serializers.CharField(
        required=True,
    )

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('last_login', 'date_joined', 'is_active')


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    profile_pic = serializers.ImageField(required=False)

    def update(self, instance, validated_data):
        if validated_data.get('password') is not None:
            validated_data['password'] = make_password(validated_data.get('password'))
            return super(UserUpdateSerializer, self).update(instance, validated_data)
        else:
            return super(UserUpdateSerializer, self).update(instance, validated_data)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('last_login', 'date_joined', 'is_active')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('view', 'like', 'owner')


class TokenObtainPairPatchedSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['is_staff'] = self.user.is_staff
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['user_id'] = self.user.user_id
        self.user.last_login = timezone.now()
        self.user.save()
        return data
