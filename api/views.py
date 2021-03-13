import logging

from django.contrib.auth.models import Group
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, AllowAny, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from api.group_permissions import IsUserSelf, IsOwnerOrReadOnly
from api.models import User, Post
from api.serializers import UserSerializer, UserUpdateSerializer, GroupSerializer, PostSerializer

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    serializer_update_class = UserUpdateSerializer

    def dispatch(self, request, *args, **kwargs):
        return super(UserViewSet, self).dispatch(request, *args, **kwargs)

    def list(self, request):
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            logger.error(serializer.errors)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset.all(), pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        serializer = self.serializer_update_class(self.queryset.get(user_id=pk), data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            logger.error(serializer.errors)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset.all(), pk=pk)
        user.is_active = False
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminUser, IsUserSelf]
        return [permission() for permission in permission_classes]


class GroupViewSet(viewsets.ViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def dispatch(self, request, *args, **kwargs):
        return super(GroupViewSet, self).dispatch(request, *args, **kwargs)

    def list(self, request):
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            logger.error(serializer.errors)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        group = get_object_or_404(self.queryset.all(), pk=pk)
        serializer = self.serializer_class(group)
        return Response(serializer.data)

    def update(self, request, pk=None):
        serializer = self.serializer_class(self.queryset.get(group_id=pk), data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            logger.error(serializer.errors)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        group = get_object_or_404(self.queryset.all(), pk=pk)
        group.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


class PostViewSet(viewsets.ViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def dispatch(self, request, *args, **kwargs):
        return super(PostViewSet, self).dispatch(request, *args, **kwargs)

    def list(self, request):
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=request.user)
        else:
            logger.error(serializer.errors)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.queryset.all(), pk=pk)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def update(self, request, pk=None):
        serializer = self.serializer_class(self.queryset.get(post_id=pk), data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            logger.error(serializer.errors)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        post = get_object_or_404(self.queryset.all(), pk=pk)
        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method in SAFE_METHODS:
            permission_classes = [AllowAny]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsOwnerOrReadOnly]

        return [permission() for permission in permission_classes]
