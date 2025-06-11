# accounts/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, nickname=None, **extra_fields):
        user = self.model(username=username, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, nickname=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, nickname, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)  # unique=True 추가
    password = models.CharField(max_length=128)  # 암호화된 비밀번호
    nickname = models.CharField(max_length=100, blank=True, null=True)  # 닉네임 필드    

    USERNAME_FIELD = 'username'  # 유저를 인증할 때 사용할 필드 (username)

    objects = CustomUserManager()  # 위에서 작성한 사용자 매니저를 사용

    def __str__(self):
        return self.username
