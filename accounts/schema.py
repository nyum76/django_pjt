from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object


class JWTAuthScheme(OpenApiAuthenticationExtension):
    target_class = "app.auth.JWTAuthentication"
    name = "JWTAuth"

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name='Authorization',
            token_prefix='Bearer'
        )