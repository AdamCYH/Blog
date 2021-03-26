import logging

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import User
from api.tests import tests_helper
from testing import truth

logger = logging.getLogger('django_test')
logger.info('Unit test logger enabled.')

user_base_url = '/api/user/'


class UserTests(APITestCase):

    # TODO(adam): Add test cases on changing user password.

    def test_createUser_anonymous_shouldCreateUser(self):
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

    def test_listUser_admin_shouldReturn3Users(self):
        # Arrange
        tests_helper.create_fake_admin_user()
        tests_helper.create_fake_users()

        # Act
        tests_helper.login_as_admin(self)
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

    def test_listUser_Anonymous_shouldReturnUnauthorized(self):
        # Arrange
        tests_helper.create_fake_users()

        # Act
        actual = self.client.get(user_base_url, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_listUser_loggedInUser_shouldReturnUnauthorized(self):
        # Arrange
        tests_helper.create_fake_users()

        # Act
        tests_helper.login_as_user_1(self)
        actual = self.client.get(user_base_url, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieveUser_loggedInUser_shouldRetrieveUser(self):
        # Arrange
        tests_helper.create_fake_admin_user()
        user1, user2 = tests_helper.create_fake_users()

        # Act
        tests_helper.login_as_user_1(self)
        actual = self.client.get(user_base_url + str(user2.user_id) + "/", format='json')

        # Assert
        expected = {"user_id": str(user2.user_id), "profile_pic": "/media/default_profile.jpeg",
                    "username": "user-2", "email": "user-2@gmail.com", "last_login": "#####", "is_superuser": False,
                    "first_name": "fname-2", "last_name": "lname-2", "is_staff": False, "is_active": True,
                    "date_joined": "#####", "user_permissions": [], "groups": []}

        self.assertEqual(actual.status_code, status.HTTP_200_OK)
        truth.assert_that_ignore_fields(self,
                                        actual,
                                        expected,
                                        ['date_joined', 'last_login'],
                                        ignore_order=True)

    def test_retrieveUser_anonymous_shouldReturnUnauthorized(self):
        # Arrange
        user1, user2 = tests_helper.create_fake_users()

        # Act
        actual = self.client.get(user_base_url + str(user1.user_id) + "/", format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_updateUser_self_shouldUpdateUser(self):
        # Arrange
        user1, user2 = tests_helper.create_fake_users()
        request_data = {"username": user1.username,
                        "email": "updated@gmail.com",
                        "first_name": user1.first_name,
                        "last_name": user1.last_name}

        # Act
        tests_helper.login_as_user_1(self)
        actual = self.client.put(user_base_url + str(user1.user_id) + "/", data=request_data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(user_id=user1.user_id).email, "updated@gmail.com")

    def test_updateUser_self_shouldIgnoreAdminFields(self):
        # Arrange
        user1, user2 = tests_helper.create_fake_users()
        request_data = {"username": user1.username,
                        "email": user1.email,
                        "first_name": user1.first_name,
                        "last_name": user1.last_name,
                        "is_superuser": True,
                        "is_active": False}

        # Act
        tests_helper.login_as_user_1(self)
        actual = self.client.put(user_base_url + str(user1.user_id) + "/", data=request_data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(user_id=user1.user_id).is_superuser, False)
        self.assertEqual(User.objects.get(user_id=user1.user_id).is_active, True)

    def test_updateUser_admin_shouldUpdateEverything(self):
        # Arrange
        tests_helper.create_fake_admin_user()
        user1, user2 = tests_helper.create_fake_users()
        request_data = {"username": user1.username,
                        "email": user1.email,
                        "first_name": user1.first_name,
                        "last_name": user1.last_name,
                        "is_superuser": True,
                        "is_active": False}

        # Act
        tests_helper.login_as_admin(self)
        actual = self.client.put(user_base_url + str(user1.user_id) + "/", data=request_data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(user_id=user1.user_id).is_superuser, True)
        self.assertEqual(User.objects.get(user_id=user1.user_id).is_active, False)

    def test_updateUser_loggedInUser_shouldNotUpdateOtherUser(self):
        # Arrange
        user1, user2 = tests_helper.create_fake_users()
        request_data = {"username": ""}

        # Act
        tests_helper.login_as_user_1(self)
        actual = self.client.put(user_base_url + str(user2.user_id) + "/", data=request_data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_403_FORBIDDEN)

    def test_updateUser_anonymous_shouldReturnUnauthorized(self):
        # Arrange
        user1, user2 = tests_helper.create_fake_users()
        request_data = {"username": ""}

        # Act
        actual = self.client.put(user_base_url + str(user1.user_id) + "/", data=request_data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deleteUser_self_shouldMarkInactive(self):
        # Arrange
        user1, user2 = tests_helper.create_fake_users()

        # Act
        tests_helper.login_as_user_1(self)
        actual = self.client.delete(user_base_url + str(user1.user_id) + "/", format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.get(user_id=user1.user_id).is_active, False)

    def test_deleteUser_admin_shouldMarkInactive(self):
        # Arrange
        tests_helper.create_fake_admin_user()
        user1, user2 = tests_helper.create_fake_users()

        # Act
        tests_helper.login_as_admin(self)
        actual = self.client.delete(user_base_url + str(user1.user_id) + "/", format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.get(user_id=user1.user_id).is_active, False)

    def test_deleteUser_loggedInUser_shouldNotDeleteOtherUser(self):
        # Arrange
        user1, user2 = tests_helper.create_fake_users()

        # Act
        tests_helper.login_as_user_1(self)
        actual = self.client.delete(user_base_url + str(user2.user_id) + "/", format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_403_FORBIDDEN)

    def test_deleteUser_anonymous_shouldReturnUnauthorized(self):
        # Arrange
        user1, user2 = tests_helper.create_fake_users()
        request_data = {"username": ""}

        # Act
        actual = self.client.put(user_base_url + str(user1.user_id) + "/", data=request_data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_401_UNAUTHORIZED)
