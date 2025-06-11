# django_pjt

## 기능
- 회원가입
- 로그인
- 로그아웃 (JWT 인증)

## 테스트
Postman 으로 먼저 진행하였고 이후에 Pytest도 진행

## 트러블슈팅
### 1
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