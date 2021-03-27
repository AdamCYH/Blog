import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from api.utils import get_video_upload_path, get_audio_upload_path, get_image_upload_path


class Group(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        db_table = 'group'


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'password']
    # TODO(adam): Make sure the image path is accurate.
    profile_pic = models.ImageField(default='default_profile.jpeg')  # set up default pic
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    groups = models.ManyToManyField(
        Group,
        blank=True,
        through='UserGroup',
    )

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'


class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_group")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="user_group")

    class Meta:
        db_table = 'user_group'


class Category(models.Model):
    # TODO(adam): Make primary key id.
    name = models.CharField(primary_key=True, max_length=100)
    createdBy = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='categories',
    )

    class Meta:
        db_table = 'category'


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True)
    body = models.TextField(null=True)
    video = models.FileField(upload_to=get_video_upload_path, null=True)
    audio = models.FileField(upload_to=get_audio_upload_path, null=True)

    author = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts"
    )

    view = models.BigIntegerField(default=0)
    is_public = models.BooleanField(default=False)
    like = models.IntegerField(default=0)

    createdTimestamp = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    lastUpdatedTimestamp = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post'


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=get_image_upload_path)
    name = models.CharField(max_length=100)
    is_public = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='images',
    )
    createdTimestamp = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        db_table = 'image'
