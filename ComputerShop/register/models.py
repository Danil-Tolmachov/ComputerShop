import json
from json import JSONDecodeError

from django.contrib import admin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, EmailField, ForeignKey, DateTimeField, BooleanField, ManyToManyField, JSONField
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone

from cart.models import Order, ProductItem
from core.models import Notification
from register.utils import send_verify_email


class ShopUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        if not user.is_superuser:
            send_verify_email(user, email)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        # need to verificate if default user
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

    cart = ManyToManyField(ProductItem, related_name='user')
    orders = ManyToManyField(Order, blank=True, related_name='shopuser')

    # Uses json.dump() and json.loads() to manipulate with resent objects
    resents = models.CharField(max_length=200, blank=True)

    notifications = JSONField()
    date_joined = DateTimeField(default=timezone.now)

    is_active = BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ShopUserManager()

    def __str__(self):
        return self.email

    def get_added_resents(self, product):

        try:
            resents = json.loads(str(self.resents))
        except JSONDecodeError:
            resents = []

        if product in resents:
            resents.remove(product)
            resents.append(product)
        else:
            resents.append(product)

        return json.dumps(resents[-10:])

    def get_resents(self):
        return json.loads(self.resents)

    def get_order(self, request, order_url):
        self.order = Order.objects.create(url=order_url)
        self.order.products.add(*request.user.cart.all())

        return self.order

    @admin.display(description='Active orders')
    def get_active_orders_count(self):
        return self.orders.filter(is_closed=False).count()

