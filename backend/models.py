from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    u_name = models.CharField(max_length=50)


class Department(models.Model):
    d_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    d_name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.d_name


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    s_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    s_pwd = models.CharField(max_length=30, blank=True, null=True)
    s_name = models.CharField(max_length=30, blank=True, null=True)
    s_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    s_email = models.CharField(max_length=30, blank=True, null=True)
    s_phone = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.s_name


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    t_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    t_pwd = models.CharField(max_length=30, blank=True, null=True)
    t_name = models.CharField(max_length=30, blank=True, null=True)
    t_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    t_email = models.CharField(max_length=30, blank=True, null=True)
    t_phone = models.CharField(max_length=30, blank=True, null=True)
    t_office = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.t_name


class Course(models.Model):
    c_name = models.CharField(max_length=30, blank=True, null=True, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.RESTRICT)
    intro = models.CharField(max_length=30, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True, default=30)
    confirmed = models.BooleanField(default=False)

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
    isSelect = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.student.s_name

class PostTheme(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    title = models.CharField(max_length=30, blank=True, null=True)
    content = models.CharField(max_length=300, blank=True, null=True)
    time = models.CharField(max_length=30, blank=True, null=True)
    isExcellent = models.IntegerField(blank=True, null=True, default=0)
    likedNum = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.content

class Liked(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    post_theme = models.ForeignKey(PostTheme, on_delete=models.RESTRICT)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    content = models.CharField(max_length=300, blank=True, null=True)
    time = models.CharField(max_length=30, blank=True, null=True)
    post_theme = models.ForeignKey(PostTheme, on_delete=models.CASCADE)

    def __str__(self):
        return self.content





