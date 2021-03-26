import logging

from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import User
from testing import truth

logger = logging.getLogger('django_test')
logger.info('Unit test logger enabled.')

user_base_url = '/api/user/'
fake_admin_username = 'fake-admin'
fake_admin_password = 'fake-admin'


class UserTests(APITestCase):

    def test_create_user__should_create_user(self):
        # Arrange
        data = {'username': 'username',
                'password': 'password',
                'email': 'email@gmail.com',
                'first_name': 'fname',
                'last_name': 'lname'}

        # act
        actual = self.client.post(user_base_url, data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'username')
        self.assertEqual(User.objects.get().email, 'email@gmail.com')
        self.assertEqual(User.objects.get().first_name, 'fname')
        self.assertEqual(User.objects.get().last_name, 'lname')

    def test_list_user__admin__should_return_3(self):
        # Arrange
        self.create_fake_admin_user()
        self.create_fake_users()

        # Act
        self.client.login(username=fake_admin_username, password=fake_admin_password)
        actual = self.client.get(user_base_url, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_200_OK)
        expected = [{"user_id": "#####", "profile_pic": "/media/default_profile.jpeg",
                     "username": "user-2", "email": "user-2@gmail.com", "last_login": "#####", "is_superuser": False,
                     "first_name": "fname-2", "last_name": "lname-2", "is_staff": False, "is_active": True,
                     "date_joined": "#####", "user_permissions": [], "groups": []},
                    {"user_id": "#####", "profile_pic": "/media/default_profile.jpeg",
                     "username": "user-1", "email": "user-1@gmail.com", "last_login": "#####", "is_superuser": False,
                     "first_name": "fname-1", "last_name": "lname-1", "is_staff": False, "is_active": True,
                     "date_joined": "#####", "user_permissions": [], "groups": []},
                    {"user_id": "#####", "profile_pic": "/media/default_profile.jpeg",
                     "username": "fake-admin", "email": "", "last_login": "#####", "is_superuser": True,
                     "first_name": "", "last_name": "", "is_staff": True, "is_active": True,
                     "date_joined": "#####", "user_permissions": [], "groups": []}]
        truth.assert_that_ignore_fields(self,
                                        actual,
                                        expected,
                                        ['user_id', 'date_joined', 'last_login'],
                                        ignore_order=True)

    def test_list_user__anonymous__should_return_unauthorized(self):
        # Arrange
        self.create_fake_users()

        # Act
        actual = self.client.get(user_base_url, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_user__normal_user__should_return_unauthorized(self):
        # Arrange
        user1, user2 = self.create_fake_users()

        # Act
        self.client.login(username="user-1", password="user-1")
        actual = self.client.get(user_base_url, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user__logged_in_user__should_retrieve_user(self):
        # Arrange
        self.create_fake_admin_user()
        user1, user2 = self.create_fake_users()

        # Act
        self.client.login(username="user-2", password="user-2")
        actual = self.client.get(user_base_url + str(user1.user_id) + "/", format='json')
        # Assert
        expected = {"user_id": str(user1.user_id), "profile_pic": "/media/default_profile.jpeg",
                    "username": "user-1", "email": "user-1@gmail.com", "last_login": "#####", "is_superuser": False,
                    "first_name": "fname-1", "last_name": "lname-1", "is_staff": False, "is_active": True,
                    "date_joined": "#####", "user_permissions": [], "groups": []}

        self.assertEqual(actual.status_code, status.HTTP_200_OK)
        truth.assert_that_ignore_fields(self,
                                        actual,
                                        expected,
                                        ['date_joined', 'last_login'],
                                        ignore_order=True)

    def test_retrieve_user__anonymous__should_return_unauthorized(self):
        # Arrange
        user1, user2 = self.create_fake_users()

        # Act
        actual = self.client.get(user_base_url + str(user1.user_id) + "/", format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user__self__should_update_user(self):
        # Arrange
        user1, user2 = self.create_fake_users()

        # Act
        self.client.login(username="user-1", password="user-1")
        request_data = {"username": user1.username,
                        "email": "updated@gmail.com",
                        "first_name": user1.first_name,
                        "last_name": user1.last_name, "is_superuser": True}
        actual = self.client.put(user_base_url + str(user1.user_id) + "/", data=request_data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(user_id=user1.user_id).email, "updated@gmail.com")

    def test_update_user__self__should_ignore_admin_fields(self):
        # Arrange
        user1, user2 = self.create_fake_users()

        # Act
        self.client.login(username="user-1", password="user-1")
        request_data = {"username": user1.username,
                        "email": user1.email,
                        "first_name": user1.first_name,
                        "last_name": user1.last_name, "is_superuser": True, "is_active": False}
        actual = self.client.put(user_base_url + str(user1.user_id) + "/", data=request_data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(user_id=user1.user_id).is_superuser, False)
        self.assertEqual(User.objects.get(user_id=user1.user_id).is_active, True)

    def test_update_user__admin__should_update_everything(self):
        # Arrange
        self.create_fake_admin_user()
        user1, user2 = self.create_fake_users()

        # Act
        self.client.login(username=fake_admin_username, password=fake_admin_password)
        request_data = {"username": user1.username,
                        "email": user1.email,
                        "first_name": user1.first_name,
                        "last_name": user1.last_name, "is_superuser": True, "is_active": False}
        actual = self.client.put(user_base_url + str(user1.user_id) + "/", data=request_data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(user_id=user1.user_id).is_superuser, True)
        self.assertEqual(User.objects.get(user_id=user1.user_id).is_active, False)

    def test_update_user__anonymous__should_return_unauthorized(self):
        # Arrange
        user1, user2 = self.create_fake_users()

        # Act
        request_data = {"username": ""}
        actual = self.client.put(user_base_url + str(user1.user_id) + "/", data=request_data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def create_fake_admin_user():
        User.objects.create_superuser(username=fake_admin_username, password=fake_admin_password)

    @staticmethod
    def create_fake_users():
        user1 = User.objects.create(username='user-1',
                                    password=make_password('user-1'),
                                    email='user-1@gmail.com',
                                    first_name='fname-1',
                                    last_name='lname-1')
        user2 = User.objects.create(username='user-2',
                                    password=make_password('user-2'),
                                    email='user-2@gmail.com',
                                    first_name='fname-2',
                                    last_name='lname-2')
        return user1, user2
