# django_pjt

- [x] 회원가입 기능
- [x] 로그인 기능
- [x] 로그아웃 기능
- [x] swagger 기능
  - [ ] 트러블슈팅 2 - Authorize 버튼 해결
- [x] 배포
- [x] Postman 테스트
- [x] Pytest 테스트
  - [x] 트러블슈팅 1 - token expired 통과

---
## AWS EC2 서버 배포
[서버 링크](http://43.200.101.60:8000/swagger/)

http://43.200.101.60:8000/

## 기능
> 테스트는 Postman 으로 진행됨
### 회원가입
- endpoint : `signup/`
- 회원가입 성공
```
{
"username": "JIN HO",
"nickname": "Mentos"
}
```
![회원가입 성공](/img/signup_success.png)

- 회원가입 실패
```
{
  "error": {
  "code": "USER_ALREADY_EXISTS" ,
  "message": 이미 가입된 사용자입니다.
  }
}
```
![회원가입 실패](/img/signup_failed.png)


### 로그인
- endpoint : `login/`
- 로그인 성공
```
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ5NzE4MzQzLCJpYXQiOjE3NDk3MTgwNDMsImp0aSI6IjYzYzc2MWU2YzI0ZTQ5MWJhZDBlMzdiNjdjYmQwMzhmIiwidXNlcl9pZCI6N30.iJjYD8-5er4u6H2JDVVGUCw9WM_M5d8UWuOulVn2REU"
}
```
![로그인 성공](/img/login_failed.png)

- 로그인 실패
```
{
    "error": {
        "code": "INVALID_CREDENTIALS",
        "message": "아이디 또는 비밀번호가 올바르지 않습니다."
    }
}
```
![로그인 실패](/img/login_failed.png)

### 로그아웃 (JWT 인증)
- endpoint : `logout/`
- 로그아웃 성공

![로그아웃 성공](/img/logout_success.png)

- 토큰 만료
```
{
    "error": {
        "code": "TOKEN_EXPIRED",
        "message": "토큰이 만료되었습니다."
    }
}
```

![토큰 만료](/img/token_expired.png)


- 토큰 없음
```
{
    "error": {
        "code": "TOKEN_NOT_FOUND",
        "message": "토큰이 없습니다."
    }
}
```
![토큰 없음](/img/token_not_found.png)


- 유효하지 않은 토큰
```
{
    "error": {
        "code": "INVALID_TOKEN",
        "message": "토큰이 유효하지 않습니다."
    }
}
```
![유효하지 않은 토큰](/img/invalid_token.png)

  
### swagger
- endpoint : `swagger/`
![swagger](/img/swagger.png)

### Pytest 진행법
manage.py 와 같은 레벨의 디렉토리(`django_pjt`)에서 아래명령어 입력
```zsh
pytest
```

## 트러블슈팅
### 1

<details>
<summary><b>Pytest - test_logout_expired_token 실패</b></summary>
<div markdown="1">

<details>
<summary><b>Pytest 진행 내용 - 실패</b></summary>
<div markdown="1">

```zsh
❯ pytest
========================================== test session starts ===========================================
platform darwin -- Python 3.10.10, pytest-8.4.0, pluggy-1.6.0
django: version: 4.2, settings: django_pjt.settings (from ini)
rootdir: /Users/nyum76/Documents/project/django_pjt
configfile: pytest.ini
plugins: django-4.11.1
collected 7 items                                                                                        

accounts/test_accounts.py ......F                                                                  [100%]

================================================ FAILURES ================================================
_______________________________________ test_logout_expired_token ________________________________________

settings = <pytest_django.fixtures.SettingsWrapper object at 0x1076f7df0>

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
>       assert response.status_code == 401
E       assert 200 == 401
E        +  where 200 = <Response status_code=200, "application/json">.status_code

accounts/test_accounts.py:111: AssertionError
======================================== short test summary info =========================================
FAILED accounts/test_accounts.py::test_logout_expired_token - assert 200 == 401
====================================== 1 failed, 6 passed in 3.12s =======================================
```

</div>
</details>

Postman 에서는 만료된 토큰으로 로그아웃시 아래와 같이 떴는데
```
{
    "error": {
        "code": "TOKEN_EXPIRED",
        "message": "토큰이 만료되었습니다."
    }
}
```

Pytest 로 진행했을 때 401 로 나와야할 게 200 OK 이 되어버림

---

SIMPLE_JWT 설정 변경이 토큰 발급에 반영되지 않음
`@override_settings(SIMPLE_JWT=...)`는 Django의 settings만 바꿈
하지만 `rest_framework_simplejwt`는 내부적으로 settings를 캐싱함
Pytest에서 settings를 바꿔도, 이미 임포트된 시점의 설정이 계속 사용될 수 있음..
즉, 토큰을 발급할 때 실제로는 여전히 기본 만료시간(1분)이 적용되고,
테스트에서 2초 기다려도 토큰이 만료되지 않은 상태가 됨.

➡️ `settings.py` 의 ACCESS_TOKEN_LIFETIME 값을 1분에서 1초로 변경

```py
# 변경 전
"ACCESS_TOKEN_LIFETIME": timedelta(minutes=1),

# 변경 후
"ACCESS_TOKEN_LIFETIME": timedelta(seconds=1),
```

<details>
<summary><b>Pytest 진행 내용 - 성공</b></summary>
<div markdown="1">

```zsh
❯ pytest
========================================== test session starts ===========================================
platform darwin -- Python 3.10.10, pytest-8.4.0, pluggy-1.6.0
django: version: 4.2, settings: django_pjt.settings (from ini)
rootdir: /Users/nyum76/Documents/project/django_pjt
configfile: pytest.ini
plugins: django-4.11.1
collected 7 items                                                                                        

accounts/test_accounts.py .......                                                                  [100%]

=========================================== 7 passed in 2.96s ============================================
```


</div>
</details>

</div>
</details>

### 2
`drf-spectacular` 를 사용하면 따로 설정할 필요 없이 swagger 페이지에서 `Authorize` 버튼이 상단에 보여야 하는데 없음