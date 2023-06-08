from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    company_name = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=20)
    groups = models.ManyToManyField(Group, related_name='accounts_users', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='accounts_users', blank=True)