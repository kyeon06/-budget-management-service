from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from common.models import BaseModel

class UserManager(BaseUserManager):
    
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("username은 필수 입력 내용입니다.")
        
        user = self.model(
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    username = models.CharField("계정명", max_length=20, unique=True)

    is_active = models.BooleanField("활성화여부", default=True)
    is_admin = models.BooleanField("관리자여부", default=False)
    is_superuser = models.BooleanField("superuser 여부", default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username
    
    @property
    def is_staff(self):
        """ admin 권한 설정 """
        return self.is_admin


