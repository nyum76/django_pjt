from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import (
    InvalidToken, TokenError, TokenBackendExpiredToken, ExpiredTokenError
)
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Swagger, schema 요청은 인증 건너뜀
        if request.path.startswith('/swagger') or request.path.startswith('/schema'):
            return None
        header = self.get_header(request)
        if header is None:
            raise AuthenticationFailed(
                detail={
                    "error": {
                        "code": "TOKEN_NOT_FOUND",
                        "message": "토큰이 없습니다."
                    }
                },
                code=status.HTTP_401_UNAUTHORIZED
            )
        try:
            return super().authenticate(request)
        except (ExpiredTokenError, TokenBackendExpiredToken):
            raise AuthenticationFailed(
                detail={
                    "error": {
                        "code": "TOKEN_EXPIRED",
                        "message": "토큰이 만료되었습니다."
                    }
                },
                code=status.HTTP_401_UNAUTHORIZED
            )
        except InvalidToken as e:
            # 내부 메시지에 'token is expired' 또는 'expired'가 포함되어 있으면 만료로 처리
            error_str = str(e)
            if 'token is expired' in error_str.lower() or 'expired' in error_str.lower():
                raise AuthenticationFailed(
                    detail={
                        "error": {
                            "code": "TOKEN_EXPIRED",
                            "message": "토큰이 만료되었습니다."
                        }
                    },
                    code=status.HTTP_401_UNAUTHORIZED
                )
            else:
                raise AuthenticationFailed(
                    detail={
                        "error": {
                            "code": "INVALID_TOKEN",
                            "message": "토큰이 유효하지 않습니다."
                        }
                    },
                    code=status.HTTP_401_UNAUTHORIZED
                )
        except TokenError:
            raise AuthenticationFailed(
                detail={
                    "error": {
                        "code": "INVALID_TOKEN",
                        "message": "토큰이 유효하지 않습니다."
                    }
                },
                code=status.HTTP_401_UNAUTHORIZED
            )