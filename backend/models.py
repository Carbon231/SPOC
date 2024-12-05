from django.contrib.auth.models import AbstractUser
from django.db import models

class Student(models.Model):
    s_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    s_pwd = models.CharField(max_length=30, blank=True, null=True, unique=True)
    s_name = models.CharField(max_length=30, blank=True, null=True, unique=True)


class Teacher(models.Model):
    t_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    t_pwd = models.CharField(max_length=30, blank=True, null=True, unique=True)
    t_name = models.CharField(max_length=30, blank=True, null=True, unique=True)
