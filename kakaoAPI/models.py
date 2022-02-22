from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, realname):

        if not username:
            raise ValueError('must have user email')
        if not realname:
            raise ValueError('must have user nickname')

        user = self.model(
            username=username,
            realname=realname,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, username, realname, password):

        user = self.create_user(
            username=username,
            realname=realname
        )
        user.set_password(password)
        user.is_admin = True  # 슈퍼유저 권한 부여
        user.is_superuser = True  # 슈퍼유저 권한 부여
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    username = models.CharField(
        max_length=20,
        unique=True
    )
    realname = models.CharField(
        max_length=20
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['realname', ]

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin