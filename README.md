# django_pjt

- [x] 회원가입 기능
- [x] 로그인 기능
- [x] 로그아웃 기능
- [ ] swagger 기능
  - [ ] 트러블슈팅 2 - Authorize 버튼 해결
- [ ] 배포
- [x] Postman 테스트
- [x] Pytest 테스트
  - [ ] 트러블슈팅 1 - token expired 통과 문제

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

### 2
`drf-spectacular` 를 사용하면 따로 설정할 필요 없이 swagger 페이지에서 `Authorize` 버튼이 상단에 보여야 하는데 없음