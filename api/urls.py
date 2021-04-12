from django.urls import path
from rest_framework.routers import SimpleRouter

from api.views import UserViewSet, GroupViewSet, PostViewSet, ImageViewSet, CategoryViewSet, PostReadSignalView

api_router = SimpleRouter()
api_router.register(r'user', UserViewSet)
api_router.register(r'group', GroupViewSet)
api_router.register(r'post', PostViewSet, basename='post')
api_router.register(r'category', CategoryViewSet, basename='category')
api_router.register(r'image', ImageViewSet)

urlpatterns = [
    path(r'post_read_signal', PostReadSignalView.as_view(), name='post_read_heart_beat'),
]
