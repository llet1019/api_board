from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    user_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        try:
            user = self.model(
                email=self.normalize_email(email),
                provider='email',
                user_type=0,
            )
            user.is_active = True
            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            print(e)

    def create_superuser(self, email, password, **extra_fields):

        superuser = self.model(
            email=self.normalize_email(email),
            provider='email',
            user_type=0,
            password=password,
        )
        superuser.is_admin = True
        superuser.is_superuser = True
        superuser.is_active = True

        superuser.set_password(password)
        superuser.save()
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    email = models.EmailField(max_length=255, unique=False)
    is_admin = models.BooleanField(verbose_name='어드민 접근 가능', default=False)
    is_active = models.BooleanField(verbose_name='활성', default=True)
    is_superuser = models.BooleanField(default=False)
    joined_date = models.DateTimeField(verbose_name=_('Date joined'), default=timezone.now)
    login_date = models.DateTimeField(auto_now=True, verbose_name='마지막로그인', )
    login_count = models.IntegerField(blank=True, null=True, default=0, verbose_name='로그인수', )
    uid = models.CharField(max_length=256, null=True, verbose_name='uid', )
    nickname = models.CharField(max_length=100, blank=True, null=True, verbose_name='닉네임', )
    username = models.CharField(max_length=100, blank=True, null=True, verbose_name='이름', )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='폰', )
    fcm_token = models.CharField(max_length=255, blank=True, null=True, verbose_name='푸시토큰', )
    uuid = models.UUIDField(blank=True, null=True, unique=True, verbose_name='UUID')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('id',)

    def __str__(self):
        return self.email
