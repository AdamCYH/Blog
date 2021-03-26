from django.contrib.auth.hashers import make_password

from api.models import User

fake_admin_username = 'fake-admin'
fake_admin_password = 'fake-admin'


def login_as_admin(test_case):
    test_case.client.login(username=fake_admin_username, password=fake_admin_password)


def login_as_user_1(test_case):
    test_case.client.login(username='user-1', password='user-1')


def create_fake_admin_user():
    User.objects.create_superuser(username=fake_admin_username, password=fake_admin_password)


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
