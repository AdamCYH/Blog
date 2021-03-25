import os
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from api.utils import random_string


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'password']
    profile_pic = models.ImageField(default='default_profile.jpeg')  # set up default pic
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user', args=[str(self.id)])


class Category(models.Model):
    name = models.CharField(max_length=100)
    createdBy = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='categories',
    )

    class Meta:
        db_table = 'category'


def get_video_upload_path(instance, filename):
    name = filename.split('.')[0]
    ext = filename.split('.')[1]
    return os.path.join(
        "user_%s" % instance.owner.user_id, "videos", "{}_{}.{}".format(name, random_string(5), ext))


def get_audio_upload_path(instance, filename):
    name = filename.split('.')[0]
    ext = filename.split('.')[1]
    return os.path.join(
        "user_%s" % instance.owner.user_id, "audios", "{}_{}.{}".format(name, random_string(5), ext))


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True)
    body = models.TextField()
    video = models.FileField(upload_to=get_video_upload_path)
    audio = models.FileField(upload_to=get_audio_upload_path)

    owner = models.ForeignKey(
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
        related_name="posts")

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


def get_image_upload_path(instance, filename):
    name = filename.split('.')[0]
    ext = filename.split('.')[1]
    return os.path.join(
        "user_%s" % instance.owner.user_id, "images", "{}_{}.{}".format(name, random_string(5), ext))


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=get_image_upload_path)
    name = models.CharField(max_length=100)
    is_public = models.BooleanField(default=True)
    owner = models.ForeignKey(
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
