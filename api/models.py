from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(user_name, password, **other_fields)

    def create_user(self, user_name, password, **other_fields):

        user = self.model(user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('helper', 'helper'),
        ('helped', 'helped'),
    )

    # 필요한 추가 컬럼
    user_name = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    nick_name = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=100)

    img = models.ImageField(upload_to='user_img', null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='helper')

    # 건들면 안되는거
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomAccountManager()

    # 유동적으로
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return self.user_name


class UserReview(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    score = models.IntegerField()
    review = models.TextField()

    def __str__(self):
        return self.user.user_name


class Service(models.Model):
    STATUS_CHOICES = (
        ('wait', 'wait'),
        ('proceed', 'proceed'),
        ('success', 'success'),
    )

    CATEGORY_CHOICES = (
        ('public_service', 'public_service'),
        ('phone', 'phone'),
        ('computer', 'computer'),
        ('print', 'print'),
    )

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    voice_file = models.FileField(upload_to='voice_file', null=True, blank=True)
    context = models.TextField()

    helper_phone_number = models.CharField(max_length=15, null=True, blank=True)
    helped_phone_number = models.CharField(max_length=15, null=True, blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='wait')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
