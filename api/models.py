import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'password']
    profile_pic = models.ImageField(default='default_profile.jpeg')  # set up default pic
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user', args=[str(self.id)])


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    owner = models.ForeignKey(
        User,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='blogs',
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
