from django.contrib import admin
from backend.models import Teacher
from backend.models import Student
from backend.models import Course
from backend.models import Comment
from backend.models import SC
from backend.models import Post
from backend.models import PostTheme
from backend.models import Department
from backend.models import User

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(PostTheme)
admin.site.register(SC)
admin.site.register(Department)
admin.site.register(User)