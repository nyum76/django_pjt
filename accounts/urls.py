from django.urls import path
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
)
from .views import SignupView, LoginView, LogoutView

urlpatterns = [
  path('signup/', SignupView.as_view(), name='signup'),
  path('login/', LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
]