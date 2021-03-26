import logging

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Group
from api.tests import tests_helper

logger = logging.getLogger('django_test')
logger.info('Unit test logger enabled.')

group_base_url = '/api/group/'


class GroupTests(APITestCase):

    def test_create_group__admin__should_create_group(self):
        # Arrange
        tests_helper.create_fake_admin_user()
        data = {'name': 'group-1'}

        # act
        tests_helper.login_as_admin(self)
        actual = self.client.post(group_base_url, data, format='json')

        # assert
        self.assertEqual(actual.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(Group.objects.get().name, 'group-1')
