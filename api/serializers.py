from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import User, Post, Image, Group, UserGroup, Category


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False)
    username = serializers.CharField(required=True)

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

    def update(self, instance, validated_data):
        if validated_data.get('password') is not None:
            validated_data['password'] = make_password(validated_data.get('password'))

        return super(UserSerializer, self).update(instance, validated_data)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = (
            'last_login', 'date_joined', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')


class UserUpdateSerializer(UserSerializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(
        write_only=True,
        required=False,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = (
            'username', 'last_login', 'date_joined', 'is_active', 'is_staff', 'is_superuser', 'groups',
            'user_permissions')


class UserAdminSerializer(UserSerializer):
    groups = UserGroupSerializer(many=True, required=False)

    password = serializers.CharField(
        write_only=True,
        required=False,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('last_login', 'date_joined', "user_permissions")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('createdBy',)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('view', 'like', 'owner')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
        read_only_fields = ('owner', 'name',)


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
