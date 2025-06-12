# django_pjt

- [x] 회원가입 기능
- [x] 로그인 기능
- [x] 로그아웃 기능
- [x] swagger 기능
  - [ ] 트러블슈팅 2 - Authorize 버튼 해결
- [ ] 배포
- [x] Postman 테스트
- [x] Pytest 테스트
  - [x] 트러블슈팅 1 - token expired 통과

---
## AWS EC2 서버 배포
* 아직 안 함 해야함.
[서버 링크]()

## 기능
### 회원가입
- endpoint : `signup/`
- 

### 로그인
- endpoint : `login/`
- 
### 로그아웃 (JWT 인증)
- endpoint : `logout/`
- 
### swagger
- endpoint : `swagger/`

## 테스트
Postman 으로 먼저 진행하였고 이후에 Pytest도 진행

## 트러블슈팅
### 1

<details>
<summary><b>Pytest - test_logout_expired_token 실패</b></summary>
<div markdown="1">


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


</div>
</details>

### 2
`drf-spectacular` 를 사용하면 따로 설정할 필요 없이 swagger 페이지에서 `Authorize` 버튼이 상단에 보여야 하는데 없음