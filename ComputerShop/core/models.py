from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models import CharField, EmailField, DateTimeField, BooleanField, ForeignKey, IntegerField, JSONField, \
    ManyToManyField, DateField, URLField, ImageField, TextField
from django.utils import timezone

from cart.models import Cart
from register.utils import send_verify_email


class ShopUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.cart = Cart.objects.create()
        user.set_password(password)

        if not user.is_superuser:
            send_verify_email(user, email)

        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class ShopUser(AbstractUser):
    username = None
    first_name = CharField(max_length=70, null=True, blank=True)
    last_name = CharField(max_length=70, null=True, blank=True)

    country = CharField(max_length=70, null=True, blank=True)
    city = CharField(max_length=70, null=True, blank=True)
    address = CharField(max_length=255, null=True, blank=True)

    email = EmailField(max_length=255, unique=True)

    password = CharField(max_length=255)

    cart = ForeignKey(Cart, on_delete=models.CASCADE)
    notifications = ForeignKey('Notification', on_delete=models.CASCADE, null=True)
    date_joined = DateTimeField(default=timezone.now)

    is_moderator = BooleanField(default=False)
    is_active = BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ShopUserManager()

    def __str__(self):
        return self.email


class Notification(models.Model):
    user = ForeignKey('ShopUser', on_delete=models.CASCADE)

    message = TextField()
    message_date = DateTimeField(default=timezone.now)
