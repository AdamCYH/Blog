import logging

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Group
from api.tests import tests_helper
from testing import truth

logger = logging.getLogger('django_test')
logger.info('Unit test logger enabled.')

group_base_url = '/api/group/'


class GroupTests(APITestCase):

    def setUp(self):
        tests_helper.create_fake_admin_user()
        tests_helper.create_fake_users()

    def test_createGroup_admin_shouldCreateGroup(self):
        # Arrange
        data = {'name': 'group-1'}

        # act
        tests_helper.login_as_admin(self)
        actual = self.client.post(group_base_url, data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(Group.objects.get().name, 'group-1')

    def test_createGroup_anonymous_shouldReturnUnauthorized(self):
        # Arrange
        data = {'name': 'group-1'}

        # act
        actual = self.client.post(group_base_url, data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_createGroup_loggedInUser_shouldReturnUnauthorized(self):
        # Arrange
        data = {'name': 'group-1'}

        # act
        tests_helper.login_as_user_1(self)
        actual = self.client.post(group_base_url, data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_403_FORBIDDEN)

    def test_listGroup_anonymous_shouldReturnAllGroups(self):
        # Arrange
        tests_helper.create_fake_groups()

        # act
        actual = self.client.get(group_base_url, format='json')

        # assert
        expected = [{'id': 1, "name": "group-1"}, {'id': 2, "name": "group-2"}]
        self.assertEqual(actual.status_code, status.HTTP_200_OK)
        truth.assert_that(self, actual, expected, ignore_order=True)

    def test_retrieveGroup_anonymous_shouldReturnGroup(self):
        # Arrange
        group1, group2 = tests_helper.create_fake_groups()

        # act
        actual = self.client.get(group_base_url + group1.name + '/', format='json')

        # assert
        expected = {'id': 1, 'name': 'group-1'}
        self.assertEqual(actual.status_code, status.HTTP_200_OK)
        truth.assert_that(self, actual, expected, ignore_order=True)

    def test_updateGroup_admin_shouldUpdateGroup(self):
        # Arrange
        group1, group2 = tests_helper.create_fake_groups()
        request_data = {"name": "new-name"}

        # act
        tests_helper.login_as_admin(self)
        actual = self.client.put(group_base_url + group1.name + '/', data=request_data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_200_OK)
        self.assertEqual(Group.objects.all().get(id=group1.id).name, "new-name")

    def test_updateGroup_admin_duplicatedName_shouldReturnBadRequest(self):
        # Arrange
        group1, group2 = tests_helper.create_fake_groups()
        request_data = {"name": "group-2"}

        # act
        tests_helper.login_as_admin(self)
        actual = self.client.put(group_base_url + group1.name + '/', data=request_data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(actual.content.decode("utf-8"), '{"name":["group with this name already exists."]}')
        self.assertEqual(Group.objects.all().get(id=group1.id).name, "group-1")

    def test_updateGroup_loggedInUser_shouldReturnUnauthorized(self):
        # Arrange
        tests_helper.create_fake_groups()
        request_data = {'name': 'group-1'}

        # act
        tests_helper.login_as_user_1(self)
        actual = self.client.put(group_base_url, request_data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_403_FORBIDDEN)

    def test_deleteGroup_admin_shouldDeleteGroup(self):
        # Arrange
        group1, group2 = tests_helper.create_fake_groups()

        # act
        tests_helper.login_as_admin(self)
        actual = self.client.delete(group_base_url + group1.name + '/', format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleteGroup_loggedInUser_shouldReturnUnauthorized(self):
        # Arrange
        group1, group2 = tests_helper.create_fake_groups()

        # act
        tests_helper.login_as_user_1(self)
        actual = self.client.delete(group_base_url + group1.name + '/', format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_403_FORBIDDEN)
