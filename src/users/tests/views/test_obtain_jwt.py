from typing import Callable

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User

pytestmark = pytest.mark.django_db

@pytest.fixture
def refresh_jwt(api_client: APIClient) -> Callable:
    def _request(email: str, password: str):
        return api_client.post(
            reverse('users:token-obtain-pair'),
            data={'email': email, 'password': password}
        )
    return _request       

def test_obtain_jwt_with_invalid_password(refresh_jwt: Callable, user: User) -> None:
    response = refresh_jwt(user.email, 'wrongpassword')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['detail'] == 'No active account found with the given credentials'

def test_obtain_jwt_with_invalid_email(refresh_jwt: Callable, user: User) -> None:
    user.set_password('!QAZ2wsx3edc!@#%12')
    user.save()
    response = refresh_jwt('nonexistent@example.com', '!QAZ2wsx3edc!@#%12')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data['detail'] == 'No active account found with the given credentials'

@pytest.mark.parametrize(
    'payload,expected_key,expected_message',
    [
        ({'email': '', 'password': 'somepassword'}, 'email', 'This field may not be blank.'),
        ({'email': 'someemail@example.com', 'password': ''}, 'password', 'This field may not be blank.'),
    ]
)
def test_obtain_jwt_with_missing_fields(refresh_jwt: Callable, payload: dict, expected_key: str, expected_message: str) -> None:
    response = refresh_jwt(payload['email'], payload['password'])
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[expected_key][0] == expected_message

def test_successful_jwt_obtainment(refresh_jwt: Callable, user: User) -> None:
    user.set_password('!QAZ2wsx3edc!@#%12')
    user.save()
    response = refresh_jwt(user.email, '!QAZ2wsx3edc!@#%12')
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data