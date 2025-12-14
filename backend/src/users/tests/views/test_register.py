from typing import Callable

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User

pytestmark = pytest.mark.django_db

@pytest.fixture
def register(api_client: APIClient) -> Callable:
    def _request(data: dict):
        return api_client.post(reverse('users:register'), data)
    return _request

@pytest.mark.parametrize(
    'payload, expected_key, expected_message',
    [
        (
            {'email': '', 'password': 'Password123!', 'password_confirmation': 'Password123!'},
            'email',
            ['This field may not be blank.']
        ),
        (
            {'email': 'test@mail.com', 'password': '', 'password_confirmation': '!QAZ2wsx!@#$!@#'},
            'password',
            ['This field may not be blank.']
        ),
        (
            {'email': 'test@mail.com', 'password': 'Password123!', 'password_confirmation': ''},
            'password_confirmation',
            ['This field may not be blank.']
        ),
    ]
)
def test_register_user_with_missing_fields(register: Callable, payload: dict, expected_key: str, expected_message: str) -> None:
    response = register(payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[expected_key] == expected_message

def test_register_user_with_existing_email(register: Callable, user: User) -> None:
    response = register({
        'email': user.email,
        'password': '!QAZ2wsx!@#$!@#',
        'password_confirmation': '!QAZ2wsx!@#$!@#'
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['email'] == ['A user with that email already exists.']

def test_register_user_successfully(register: Callable) -> None:
    response = register({
        'email': 'newuser@mail.com',
        'password': '!QAZ2wsx!@#$!@#',
        'password_confirmation': '!QAZ2wsx!@#$!@#'
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.data
    assert 'password' not in response.data
    assert 'password_confirmation' not in response.data

def test_register_user_with_non_matching_passwords(register: Callable) -> None:
    response = register({
        'email': 'newuser@mail.com',
        'password': '!QAZ2wsx!@#$!@#',
        'password_confirmation': 'DifferentPassword123!'
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['password_confirmation'] == ["Password fields didn't match."]

@pytest.mark.parametrize(
    'invalid_email',
    [
        'plainaddress',
        '@missingusername.com',
        'username@.com',
        'username@com',
        'username@domain..com'
    ]
)
def test_register_user_with_invalid_email_format(register: Callable, invalid_email: str) -> None:
    response = register({
        'email': invalid_email,
        'password': '!QAZ2wsx!@#$!@#',
        'password_confirmation': '!QAZ2wsx!@#$!@#'
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['email'] == ['Enter a valid email address.']

@pytest.mark.parametrize(
    'weak_password',
    [
        '12345678',
        'password',
        'qwertyui',
        'letmein123',
        'abc12345'
    ]
)
def test_register_user_with_weak_password(register: Callable, weak_password: str) -> None:
    response = register({
        'email': 'newuser@mail.com',
        'password': weak_password,
        'password_confirmation': weak_password
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'password' in response.data