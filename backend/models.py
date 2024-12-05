from django.contrib.auth.models import AbstractUser
from django.db import models

class Student(models.Model):
    s_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    s_pwd = models.CharField(max_length=30, blank=True, null=True)
    s_name = models.CharField(max_length=30, blank=True, null=True)


class Teacher(models.Model):
    t_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    t_pwd = models.CharField(max_length=30, blank=True, null=True)
    t_name = models.CharField(max_length=30, blank=True, null=True)


class Course(models.Model):
    c_name = models.CharField(max_length=30, blank=True, null=True, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.RESTRICT)
    intro = models.CharField(max_length=30, blank=True, null=True)


class Comment(models.Model):
    cm_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    degree = models.CharField(max_length=30, blank=True, null=True)
    content = models.CharField(max_length=30, blank=True, null=True)
    time = models.CharField(max_length=30, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class SC(models.Model):
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)





