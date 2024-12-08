from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True, null=True, unique=True, verbose_name='昵称')
    avatar = models.CharField(max_length=30, default='', verbose_name='头像', blank=True, null=True)
    birthday = models.CharField(max_length=30, default="2003-11-21", blank=True, null=True)
    gender = models.CharField(max_length=30, default="女", blank=True, null=True)
    studentID = models.CharField(max_length=30, default="22373333", blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    hobbies = models.CharField(max_length=300, blank=True, null=True)


class Student(models.Model):
    s_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    s_pwd = models.CharField(max_length=30, blank=True, null=True)
    s_name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.s_name


class Teacher(models.Model):
    t_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    t_pwd = models.CharField(max_length=30, blank=True, null=True)
    t_name = models.CharField(max_length=30, blank=True, null=True)
    t_department = models.CharField(max_length=30, blank=True, null=True)
    t_email = models.CharField(max_length=30, blank=True, null=True)
    t_phone = models.CharField(max_length=30, blank=True, null=True)
    t_office = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.t_name

class Course(models.Model):
    c_name = models.CharField(max_length=30, blank=True, null=True, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.RESTRICT)
    intro = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.c_name

class Comment(models.Model):
    cm_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    degree = models.CharField(max_length=30, blank=True, null=True)
    content = models.CharField(max_length=300, blank=True, null=True)
    time = models.CharField(max_length=30, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

class SC(models.Model):
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.CharField(max_length=30, blank=True, null=True)
    hasScore = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.score

class PostTheme(models.Model):
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    title = models.CharField(max_length=30, blank=True, null=True)
    content = models.CharField(max_length=300, blank=True, null=True)
    time = models.CharField(max_length=30, blank=True, null=True)
    isExcellent = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.content


class Post(models.Model):
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    content = models.CharField(max_length=300, blank=True, null=True)
    time = models.CharField(max_length=30, blank=True, null=True)
    post_theme = models.ForeignKey(PostTheme, on_delete=models.CASCADE)

    def __str__(self):
        return self.content





