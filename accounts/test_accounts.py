import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.test import override_settings
from datetime import timedelta
import importlib
from rest_framework_simplejwt import settings as jwt_settings

@pytest.mark.django_db
def test_signup_success():
    client = APIClient()
    url = reverse('signup')
    data = {"username": "testuser", "password": "testpass123", "nickname": "TestNick"}
    response = client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data == {"username": "testuser", "nickname": "TestNick"}

@pytest.mark.django_db
def test_signup_duplicate():
    client = APIClient()
    url = reverse('signup')
    data = {"username": "testuser", "password": "testpass123", "nickname": "TestNick"}
    client.post(url, data, format='json')
    response = client.post(url, data, format='json')
    assert response.status_code == 400
    assert response.data == {
        "error": {
            "code": "USER_ALREADY_EXISTS",
            "message": "이미 가입된 사용자입니다."
        }
    }

@pytest.mark.django_db
def test_login_success():
    client = APIClient()
    signup_url = reverse('signup')
    login_url = reverse('login')
    data = {"username": "testuser", "password": "testpass123", "nickname": "TestNick"}
    client.post(signup_url, data, format='json')
    response = client.post(login_url, {"username": "testuser", "password": "testpass123"}, format='json')
    assert response.status_code == 200
    assert "token" in response.data
    assert isinstance(response.data["token"], str)

@pytest.mark.django_db
def test_login_fail():
    client = APIClient()
    login_url = reverse('login')
    response = client.post(login_url, {"username": "notexist", "password": "wrong"}, format='json')
    assert response.status_code == 401
    assert response.data == {
        "error": {
            "code": "INVALID_CREDENTIALS",
            "message": "아이디 또는 비밀번호가 올바르지 않습니다."
        }
    }

@pytest.mark.django_db
def test_logout_token_not_found():
    client = APIClient()
    logout_url = reverse('logout')
    response = client.post(logout_url)  # 토큰 없이 요청
    assert response.status_code == 401
    assert response.data == {
        "error": {
            "code": "TOKEN_NOT_FOUND",
            "message": "토큰이 없습니다."
        }
    }

@pytest.mark.django_db
def test_logout_invalid_token():
    client = APIClient()
    logout_url = reverse('logout')
    # 유효하지 않은 토큰
    client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')
    response = client.post(logout_url)
    assert response.status_code == 401
    assert response.data == {
        "error": {
            "code": "INVALID_TOKEN",
            "message": "토큰이 유효하지 않습니다."
        }
    }

@pytest.mark.django_db
def test_logout_expired_token(settings):
    import time
    from datetime import timedelta
    from rest_framework_simplejwt.tokens import RefreshToken
    from django.urls import reverse
    from rest_framework.test import APIClient
    from django.contrib.auth import get_user_model

    # 1. settings 변경
    settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(seconds=1)
    # 2. simplejwt settings reload
    importlib.reload(jwt_settings)

    User = get_user_model()
    user = User.objects.create_user(username="expireuser", password="expirepass", nickname="expire")
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    time.sleep(2)

    client = APIClient()
    logout_url = reverse('logout')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = client.post(logout_url)
    assert response.status_code == 401
    assert response.data == {
        "error": {
            "code": "TOKEN_EXPIRED",
            "message": "토큰이 만료되었습니다."
        }
    }