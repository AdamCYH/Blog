import logging

from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, AllowAny, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.group_permissions import IsOwnerOrReadOnly, IsUserSelfOrAdmin
from api.models import User, Post, Image, Group, Category
from api.serializers import GroupSerializer, PostSerializer, \
    TokenObtainPairPatchedSerializer, UserSerializer, UserAdminSerializer, UserUpdateSerializer, ImageSerializer, \
    CategorySerializer

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

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
        user = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(self.request, user)

        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            logger.error(serializer.errors)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset.all(), pk=pk)
        self.check_object_permissions(self.request, user)
        user.is_active = False
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
            self.serializer_class = UserSerializer
        elif self.action == 'list':
            permission_classes = [IsAdminUser]
            self.serializer_class = UserSerializer
        elif self.action == 'retrieve':
            permission_classes = [IsUserSelfOrAdmin]
            self.serializer_class = UserSerializer
        else:
            permission_classes = [IsUserSelfOrAdmin]
            if self.request.user and self.request.user.is_staff:
                self.serializer_class = UserAdminSerializer
            else:
                self.serializer_class = UserUpdateSerializer

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
        group = get_object_or_404(self.queryset.all(), name=pk)
        serializer = self.serializer_class(group)
        return Response(serializer.data)

    def update(self, request, pk=None):
        group = get_object_or_404(self.queryset.all(), name=pk)
        serializer = self.serializer_class(group, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            logger.error(serializer.errors)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        group = get_object_or_404(self.queryset.all(), name=pk)
        group.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method in SAFE_METHODS:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def dispatch(self, request, *args, **kwargs):
        return super(CategoryViewSet, self).dispatch(request, *args, **kwargs)

    def list(self, request):
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(createdBy=request.user)
        else:
            logger.error(serializer.errors)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        group = get_object_or_404(self.queryset.all(), pk=pk)
        serializer = self.serializer_class(group)
        return Response(serializer.data)

    def update(self, request, pk=None):
        serializer = self.serializer_class(self.queryset.get(id=pk), data=request.data)
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
    serializer_class = PostSerializer

    def dispatch(self, request, *args, **kwargs):
        return super(PostViewSet, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Post.objects.all()
        author = self.request.query_params.get('author', None)
        title = self.request.query_params.get('title', None)
        category = self.request.query_params.get('category', None)
        order_by = self.request.query_params.get('orderBy', None)
        if author:
            queryset = queryset.filter(owner__username__contains=author)
        if title:
            queryset = queryset.filter(title__contains=title)
        if category:
            queryset = queryset.filter(category=category)
        if order_by:
            queryset = queryset.order_by(order_by)
        return queryset

    def list(self, request):
        serializer = self.serializer_class(self.get_queryset().all(), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner=request.user)
        else:
            logger.error(serializer.errors)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(self.get_queryset().all(), pk=pk)
        if post.owner != self.request.user:
            post.view = post.view + 1
            post.save()
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def update(self, request, pk=None):
        serializer = self.serializer_class(self.get_queryset().get(id=pk), data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            logger.error(serializer.errors)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        post = get_object_or_404(self.get_queryset().all(), pk=pk)
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


class ImageViewSet(viewsets.ViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def dispatch(self, request, *args, **kwargs):
        return super(ImageViewSet, self).dispatch(request, *args, **kwargs)

    def list(self, request):
        serializer = self.serializer_class(self.queryset.all().filter(owner=request.user), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            image = serializer.save(owner=request.user)
            image.name = self.request.FILES['image'].name
            image.save()
        else:
            logger.error(serializer.errors)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        image = get_object_or_404(self.queryset.all(), pk=pk)
        serializer = self.serializer_class(image)
        return Response(serializer.data)

    def update(self, request, pk=None):
        serializer = self.serializer_class(self.queryset.get(image_id=pk), data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            logger.error(serializer.errors)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        image = get_object_or_404(self.queryset.all(), pk=pk)
        image.image.delete()
        image.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = [IsUserSelfOrAdmin]

        return [permission() for permission in permission_classes]


class TokenObtainPairPatchedView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenObtainPairPatchedSerializer

    token_obtain_pair = TokenObtainPairView.as_view()
