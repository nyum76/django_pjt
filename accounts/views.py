from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from .serializers import SignupSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .auth import CustomJWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiRequest, OpenApiTypes
from rest_framework.permissions import IsAuthenticated


class SignupView(APIView):
    authentication_classes = []
    permission_classes = []
    @extend_schema(
        summary="회원가입",
        description="""
        회원가입 API

        요청 예시:
        {
          "username": "testuser",
          "password": "password123",
          "nickname": "닉네임"
        }
        """,
        request=SignupSerializer,
        responses={
            201: OpenApiExample(
                '회원가입 성공',
                value={"username": "testuser", "nickname": "닉네임"},
                response_only=True
            ),
            400: OpenApiExample(
                '회원가입 실패',
                value={"username": ["이미 가입된 사용자입니다."]},
                response_only=True
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        
        # 요청 데이터로 serializer를 초기화
        serializer = SignupSerializer(data=request.data)
        # 유효성 검사
        if serializer.is_valid():
          # 사용자 생성
          user = serializer.save()
          # 성공 응답 반환
          return Response(
            {
              "username": user.username,
              "nickname": user.nickname,
            },status=status.HTTP_201_CREATED)

        # 유효성 검사에서 실패한 경우 에러 반환
        return Response(
            {
              "error": {
                  "code": "USER_ALREADY_EXISTS",
                  "message": "이미 가입된 사용자입니다.",
                }
            },status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    ''' 로그인 '''
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        summary="로그인",
        description="로그인을 수행하고 JWT 토큰을 반환합니다.",
        request=LoginSerializer,
        responses={
            200: OpenApiExample(
                '로그인 성공',
                value={"token": "your_jwt_token"},
                response_only=True
            ),
            401: OpenApiExample(
                '로그인 실패',
                value={
                    "error": {
                        "code": "INVALID_CREDENTIALS",
                        "message": "아이디 또는 비밀번호가 올바르지 않습니다."
                    }
                },
                response_only=True
            ),
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({
                    "token": access_token
                }, status=status.HTTP_200_OK)
        return Response({
            "error": {
                "code": "INVALID_CREDENTIALS",
                "message": "아이디 또는 비밀번호가 올바르지 않습니다."
            }
        }, status=status.HTTP_401_UNAUTHORIZED)
  

class LogoutView(APIView):
  ''' 로그아웃 '''
  authentication_classes = [CustomJWTAuthentication]
  permission_classes = [IsAuthenticated]
  @extend_schema(
    summary="로그아웃",
    description="""
    로그아웃 API

    - 이 API는 Authorization 헤더에 JWT 토큰이 필요합니다.
    - Swagger UI에서는 상단의 'Authorize' 버튼을 클릭하고
      'Bearer <발급받은 토큰>' 형식으로 입력하세요.
    """,
    request=None,
    responses={
        200: OpenApiExample(
            '로그아웃 성공',
            value={"message": "로그아웃되었습니다."},
            response_only=True
        ),
        401: OpenApiExample(
            {
              "error": {
                "code": "INVALID_TOKEN",
                "message": "토큰이 유효하지 않습니다."
              }
         }
            ,
            {
              "error": {
                "code": "TOKEN_EXPIRED",
               "message": "토큰이 만료되었습니다."
            }
         },
          {
            "error": {
              "code": "TOKEN_NOT_FOUND",
              "message": "토큰이 없습니다."
              }
          },
            response_only=True
        ),

    },    auth=[{"type": "http", "scheme": "bearer"}],
)
  def post(self, request):
      # 여기까지 왔다는 것은 인증이 이미 통과된 것!
      logout(request)
      return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_200_OK)