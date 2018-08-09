from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.core.mail import send_mail
from django.template.loader import get_template
# Create your models here.

# send_mail(subject='', message='', from_email='', recipient_list='', html_message='')


class CustomUserManager(BaseUserManager):

    def create_user(self, email, full_name=None, password=None, is_staff=False, is_admin=False, is_active=True):
        if not email:
            raise ValueError('Users must have email Address')
        if not password:
            raise ValueError('User must have Password')
        # if not full_name:
        #     raise ValueError('User must have a full name')
        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)

    def create_staffuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, full_name=None, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


class CustomUser(AbstractBaseUser):
    # username = models.CharField(max_length=100)
    full_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=250, unique=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    # can change username, but now email
    USERNAME_FIELD = 'email'

    # default required fields = email(email is default because USERNAME_FIELDS='email'), password
    REQUIRED_FIELDS = []  # 'full_name'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    # @property
    # def is_active(self):
    #     return self.active


class GuestManager(models.Manager):
    def email(self):
        return Guest.objects.only('email')


class Guest(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now=True)

    objects = GuestManager()

    def __str__(self):
        return self.email
