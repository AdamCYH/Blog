import logging

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import User
from testing import truth

logger = logging.getLogger('django_test')
logger.info('test_log')

user_base_url = '/api/user/'
admin_username = 'admin'
admin_password = 'admin'


class UserTests(APITestCase):

    def test_create_user_should_create_user(self):
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

    def test_list_user_should_return_3(self):
        # Arrange
        self.create_fake_admin_user()
        self.create_fake_users()

        # Act
        self.client.login(username=admin_username, password=admin_password)
        actual = self.client.get(user_base_url, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_200_OK)
        expected = '''
            [{"user_id": "#####", "profile_pic": "/media/default_profile.jpeg",
             "username": "user-2", "email": "user-2@gmail.com", "last_login": #####, "is_superuser": false,
             "first_name": "fname-2", "last_name": "lname-2", "is_staff": false, "is_active": true,
             "date_joined": "#####", "user_permissions": [], "groups": []},
            {"user_id": "#####", "profile_pic": "/media/default_profile.jpeg",
             "username": "user-1", "email": "user-1@gmail.com", "last_login": #####, "is_superuser": false,
             "first_name": "fname-1", "last_name": "lname-1", "is_staff": false, "is_active": true,
             "date_joined": "#####", "user_permissions": [], "groups": []},
            {"user_id": "#####", "profile_pic": "/media/default_profile.jpeg",
             "username": "admin", "email": "", "last_login": "#####", "is_superuser": true,
             "first_name": "", "last_name": "", "is_staff": true, "is_active": true,
             "date_joined": "#####", "user_permissions": [], "groups": []}]'''
        truth.assert_that_ignore_fields(self,
                                        actual,
                                        expected,
                                        ['user_id', 'date_joined', 'last_login'],
                                        ignore_order=True)

    @staticmethod
    def create_fake_admin_user():
        User.objects.create_superuser(username=admin_username, password=admin_password)

    @staticmethod
    def create_fake_users():
        User.objects.create(username='user-1', email='user-1@gmail.com', first_name='fname-1', last_name='lname-1')
        User.objects.create(username='user-2', email='user-2@gmail.com', first_name='fname-2', last_name='lname-2')
