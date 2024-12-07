from django.urls import path
from . import views

urlpatterns = [
    # Student/Teacher Info
    path('StudentLogin/', views.StudentLogin.as_view()),
    path('StudentRegister/', views.StudentRegister.as_view()),
    path('TeacherLogin/', views.TeacherLogin.as_view()),
    path('TeacherRegister/', views.TeacherRegister.as_view()),
    path('StudentChange/', views.StudentChange.as_view()),
    path('TeacherChange/', views.TeacherChange.as_view()),

    # path('AdminLogin/', views.AdminLogin.as_view()),
    path('GetStudentList/', views.GetStudentList.as_view()),
    path('GetTeacherList/', views.GetTeacherList.as_view()),
    # path('AdminChange/', views.AdminChange.as_view()),
    path('GetStudentCourseNum/', views.GetStudentCourseNum.as_view()),
    path('GetStudentCommentNum/', views.GetStudentCommentNum.as_view()),
    path('GetStudentDiscussNum/', views.GetStudentDiscussNum.as_view()),
    path('GetTeacherCourseNum/', views.GetTeacherCourseNum.as_view()),
    # path('GetTeacherDiscussNum/', views.GetTeacherDisCussNum.as_view()),
    #
    # # Course
    path('GetCourseList/', views.GetCourseList.as_view()),
    path('SelectCourse/', views.SelectCourse.as_view()),
    path('DropCourse/', views.DropCourse.as_view()),
    path('BuildCourse/', views.BuildCourse.as_view()),
    path('ChangeCourse/', views.ChangeCourse.as_view()),
    path('CancelCourse/', views.CancelCourse.as_view()),
    path('GetCourseInfo/', views.GetCourseInfo.as_view()),
    path('GetStudentCourseList/', views.GetStudentCourseList.as_view()),
    path('GetTeacherCourseList/', views.GetTeacherCourseList.as_view()),
    #
    # # Comment
    path('GetCommentList/', views.GetCommentList.as_view()),
    path('CommentCourse/', views.CommentCourse.as_view()),
    path('DeleteComment/', views.DeleteComment.as_view()),
    #
    # # Post
    path('GetPostThemeList/', views.GetPostThemeList.as_view()),
    path('BuildPostTheme/', views.BuildPostTheme.as_view()),
    path('GetPostList/', views.GetPostList.as_view()),
    path('BuildPost/', views.BuildPost.as_view()),
    path('DeletePostTheme/', views.DeletePostTheme.as_view()),
    path('DeletePost/', views.DeletePost.as_view()),
    path('GetPostTheme/', views.GetPostTheme.as_view()),
    #
    #
    # # 成绩
    path('GetDegree/', views.GetDegree.as_view()),
    path('TeacherChangeInfo/', views.TeacherChange.as_view()),

]