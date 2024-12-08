import json
from django.utils.deprecation import MiddlewareMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.models import Student, Teacher, Course, Comment, SC, PostTheme, Post


class MyCore(MiddlewareMixin):
    """
    处理HTTP响应，设置跨域请求的相关头部信息。
    Args:
        request: 请求对象，包含请求方法、请求头等信息。
        response: 响应对象，包含响应头、响应体等信息。
    Returns:
        修改后的响应对象，包含跨域请求相关的头部信息。
    """

    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = '*'
        if request.method == 'OPTIONS':
            response["Access-Control-Allow-Headers"] = 'Content-Type'
            response["Access-Control-Allow-Methods"] = 'POST, DELETE, PUT'
        return response


class StudentLogin(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        s_id = req_data['s_id']
        s_pwd = req_data['s_pwd']
        try:
            user = Student.objects.get(s_id=s_id)
        except Exception as e:
            error_response = {'error': str(e)}
            return Response({
                "code": 401,
                "error": "学号不存在"
            })
        else:
            if user.s_pwd == s_pwd:
                s_name = user.s_name
                return Response({
                    "code": 200,
                    "message": "登录成功",
                    "s_name": s_name
                })
            else:
                return Response({
                    "code": 401,
                    "error": "密码错误"
                })



class StudentRegister(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        s_name = req_data['s_name']
        s_pwd = req_data['s_pwd']
        s_pwd_confirm = req_data['s_pwd_confirm']
        s_id = req_data['s_id']
        if s_pwd != s_pwd_confirm:
            return Response({
                "code": 400,
                "error": "密码不正确"
            })
        if Student.objects.filter(s_name=s_name).exists():
            return Response({
                "code": 400,
                "error": "用户名已存在"
            })
        if Student.objects.filter(s_id=s_id).exists():
            return Response({
                "code": 400,
                "error": "学号已存在"
            })
        user = Student.objects.create(s_id=s_id, s_name=s_name, s_pwd=s_pwd)
        user.save()
        return Response({
            "code": 200,
            "message": "注册成功"
        })

class TeacherLogin(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        t_id = req_data['t_id']
        t_pwd = req_data['t_pwd']
        user = Teacher.objects.get(t_id=t_id)
        if user.t_pwd == t_pwd:
            t_name = user.t_name
            return Response({
                "code": 200,
                "message": "登录成功",
                "t_name": t_name
            })
        else:
            return Response({
                "code": 401,
                "error": "用户名或密码错误"
            })

class TeacherRegister(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        t_name = req_data['t_name']
        t_pwd = req_data['t_pwd']
        t_id = req_data['t_id']
        t_pwd_confirm = req_data['t_pwd_confirm']
        if not t_pwd_confirm == t_pwd:
            return Response({
                "code": 401,
                "message": "密码不正确"
            })
        if Teacher.objects.filter(t_name=t_name).exists():
            return Response({
                "code": 400,
                "error": "用户名已存在"
            })
        if Teacher.objects.filter(t_id=t_id).exists():
            return Response({
                "code": 400,
                "error": "工号已存在"
            })
        user = Teacher.objects.create(t_id=t_id, t_name=t_name, t_pwd=t_pwd)
        user.save()
        return Response({
            "code": 200,
            "message": "注册成功"
        })

class StudentChange(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        s_id = req_data['s_id']
        s_pwd = req_data['s_pwd']
        new_pwd_1 = req_data['new_pwd_1']
        new_pwd_2 = req_data['new_pwd_2']
        try:
            user = Student.objects.get(s_id=s_id)
        except Exception as e:
            error_response = {'error': str(e)}
            return Response({
                "code": 401,
                "message": "学号不存在",
                "error_response": error_response
            })
        if not user.s_pwd == s_pwd:
            return Response({
                "code": 402,
                "message": "密码错误"
            })
        if new_pwd_1 == new_pwd_2:
            user.s_pwd = new_pwd_1
            user.save()
            return Response({
                "code": 200,
                "message": "操作成功"
            })
        else:
            return Response({
                "code": 401,
                "message": "新密码不一致"
            })

class TeacherChange(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        t_id = req_data['t_id']
        t_pwd = req_data['t_pwd']
        new_pwd_1 = req_data['new_pwd_1']
        new_pwd_2 = req_data['new_pwd_2']
        try:
            user = Teacher.objects.get(t_id=t_id)
        except Exception as e:
            error_response = {'error': str(e)}
            return Response({
                "code": 401,
                "message": "工号不存在",
                "error_response": error_response
            })
        if not user.t_pwd == t_pwd:
            return Response({
                "code": 402,
                "message": "密码错误"
            })
        if new_pwd_1 == new_pwd_2:
            user.t_pwd = new_pwd_1
            user.save()
            return Response({
                "code": 200,
                "message": "操作成功"
            })
        else:
            return Response({
                "code": 401,
                "message": "新密码不一致"
            })

class GetTeacherCourseNum(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        t_id = req_data['t_id']
        courses = Course.objects.filter(teacher__id=t_id)
        num = len(courses)
        return Response({
            "code": 200,
            "message": "操作成功！",
            "data": {"courseNum": num}
        })


class GetStudentCommentNum(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        s_id = req_data['s_id']
        comments = Comment.objects.filter(student__s_id=s_id)
        num = len(comments)
        return Response({
            "code": 200,
            "message": "操作成功！",
            "data": {"commentNum": num}
        })


class GetStudentCourseNum(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        s_id = req_data['s_id']
        scs = SC.objects.filter(student__s_id=s_id)
        num = len(scs)
        return Response({
            "code": 200,
            "message": "操作成功！",
            "data": {"courseNum": num}
        })


class GetTeacherList(APIView):
    def get(self, request):
        teachers = Teacher.objects.all()
        data = [{"t_id": teacher.t_id, "t_name": teacher.t_name} for teacher in teachers]
        return Response({
            "code": 200,
            "message": "操作成功！",
            "data": data
        })


class GetStudentList(APIView):
    def get(self, request):
        students = Student.objects.all()
        data = [{"s_id": student.s_id, "s_name": student.s_name} for student in students]
        return Response({
            "code": 200,
            "message": "操作成功！",
            "data": data
        })



class GetCourseList(APIView):
    def get(self, request):
        course_list = Course.objects.all()
        data = []
        for course in course_list:
            sum = 0
            avgDegree = 0
            comment = Comment.objects.filter(course__id=course.id)
            if Comment.objects.filter(course__id=course.id).exists():
                for c in comment:
                    sum += int(c.degree)
                avgDegree = sum / len(comment)
            data.append({
                "c_id": course.id,
                "c_name": course.c_name,
                "t_name": course.teacher.t_name,
                "avgDegree": avgDegree,
                "intro": course.intro
            })
        return Response({
            "code": 200,
            "message": "操作成功",
            "data": data
        })


class SelectCourse(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        c_id = req_data['c_id']
        s_id = req_data['s_id']
        student = Student.objects.get(s_id=s_id)
        course = Course.objects.get(id=c_id)
        if SC.objects.filter(student=student, course=course):
            return Response({
                "code": 401,
                "message": "已经选课"
            })
        else:
            SC.objects.create(student=student, course=course)
            return Response({
                "code": 200,
                "message": "操作成功"
            })


class DropCourse(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        c_id = req_data['c_id']
        s_id = req_data['s_id']
        student = Student.objects.get(s_id=s_id)
        course = Course.objects.get(id=c_id)
        if SC.objects.filter(student=student, course=course):
            SC.objects.get(student=student, course=course).delete()
            return Response({
                "code": 200,
                "message": "操作成功"
            })
        else:
            return Response({
                "code": 401,
                "message": "不存在选课"
            })


class BuildCourse(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        c_name = req_data['c_name']
        t_id = req_data['t_id']
        teacher = Teacher.objects.get(t_id=t_id)
        if Course.objects.filter(c_name=c_name).exists():
            return Response({
                "code": 401,
                "message": "课程已存在"
            })
        else:
            Course.objects.create(teacher=teacher, c_name=c_name)
            return Response({
                "code": 200,
                "message": "操作成功"
            })


class ChangeCourse(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        c_name = req_data['c_name']
        c_id = req_data['c_id']
        t_id = req_data['t_id']
        intro = req_data['intro']
        teacher = Teacher.objects.get(t_id=t_id)
        course = Course.objects.get(id=c_id)
        if Course.objects.filter(c_name=c_name).exists():
            return Response({
                "code": 401,
                "message": "该课程名已存在"
            })
        if not Course.objects.filter(teacher=teacher, id=c_id).exists():
            return Response({
                "code": 402,
                "message": "您并没有开设该课程，请检查课程id是否正确"
            })
        else:
            course.c_name = c_name
            course.intro = intro
            course.save()
            return Response({
                "code": 200,
                "message": "操作成功"
            })


class GetCourseInfo(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        c_id = req_data['c_id']
        if not Course.objects.filter(id=c_id).exists():
            return Response({
                "code": 200,
                "message": "课程不存在"
            })
        else:
            course = Course.objects.get(id=c_id)
            return Response({
                "code": 200,
                "message": "操作成功",
                "data": {
                    "t_name": course.teacher.t_name,
                    "c_name": course.c_name,
                    "c_id": course.id,
                    "intro": course.intro
                }
            })


class CancelCourse(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        c_id = req_data['c_id']
        t_id = req_data['t_id']
        teacher = Teacher.objects.get(t_id=t_id)
        if Course.objects.filter(id=c_id, teacher=teacher).exists():
            Course.objects.get(id=c_id).delete()
            return Response({
                "code": 200,
                "message": "操作成功"
            })
        else:
            return Response({
                "code": 401,
                "message": "停课失败"
            })


class GetStudentCourseList(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        s_id = req_data['s_id']
        scs = SC.objects.filter(student__s_id=s_id)
        data = []
        for sc in scs:
            course = sc.course
            sum = 0
            avgDegree = 0
            comment = Comment.objects.filter(course__id=course.id)
            if Comment.objects.filter(course__id=course.id).exists():
                for c in comment:
                    sum += int(c.degree)
                avgDegree = sum / len(comment)
            data.append({
                "c_id": course.id,
                "c_name": course.c_name,
                "t_name": course.teacher.t_name,
                "avgDegree": avgDegree,
                "intro": course.intro,
                "hasScore": sc.hasScore
            })
        return Response({
            "code": 200,
            "message": "操作成功",
            "data": data
        })


class GetStudentCourseScore(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        s_id = req_data['s_id']
        c_id = req_data['c_id']
        if SC.objects.filter(student__s_id=s_id, course__id=c_id).exists():
            sc = SC.objects.get(student__s_id=s_id, course__id=c_id)
            return Response({
                "code": 200,
                "message": "操作成功",
                "data": {
                    "score": sc.score
                }
            })
        else:
            return Response({
                "code": 200,
                "error": "不存在该选课"
            })


class SetStudentCourseScore(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        s_id = req_data['s_id']
        c_id = req_data['c_id']
        score = req_data['score']
        if SC.objects.filter(student__s_id=s_id, course__id=c_id).exists():
            sc = SC.objects.get(student__s_id=s_id, course__id=c_id)
            sc.score = score
            sc.hasScore = 1
            sc.save()
            return Response({
                "code": 200,
                "message": "操作成功"
            })
        else:
            return Response({
                "code": 400,
                "error": "不存在该选课"
            })


class GetTeacherInfo(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        t_id = req_data['t_id']
        if Teacher.objects.filter(t_id=t_id).exists():
            teacher = Teacher.objects.get(t_id=t_id)
            data = {
                "t_office": teacher.t_office,
                "t_department": teacher.t_department,
                "t_phone": teacher.t_phone,
                "t_email": teacher.t_email
            }
            return Response({
                "code": 200,
                "message": "操作成功",
                "data": data
            })
        else:
            return Response({
                "code": 401,
                "error": "教师不存在"
            })


class GetTeacherCourseList(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        t_id = req_data['t_id']
        courses = Course.objects.filter(teacher__t_id=t_id)
        data = []
        for course in courses:
            sum = 0
            avgDegree = 0
            comment = Comment.objects.filter(course__id=course.id)
            if Comment.objects.filter(course__id=course.id).exists():
                for c in comment:
                    sum += int(c.degree)
                avgDegree = sum / len(comment)
            data.append({
                "c_id": course.id,
                "c_name": course.c_name,
                "t_name": course.teacher.t_name,
                "avgDegree": avgDegree,
                "intro": course.intro
            })
        return Response({
            "code": 200,
            "message": "操作成功",
            "data": data
        })


class CommentCourse(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        c_id = req_data['c_id']
        s_id = req_data['s_id']
        s_name = req_data['s_name']
        degree = req_data['degree']
        content = req_data['content']
        time = req_data['time']
        # 检查课程是否存在
        try:
            course = Course.objects.get(id=c_id)
        except Course.DoesNotExist:
            return Response({
                "code": 400,
                "message": "课程不存在"
            })
        # 检查学生是否存在
        try:
            student = Student.objects.get(s_id=s_id)
        except Student.DoesNotExist:
            return Response({
                "code": 400,
                "message": "学生不存在"
            })
        Comment.objects.create(student=student,course=course,
                                         degree=degree,content=content,time=time)
        return Response({
            "code": 200,
            "message": "操作成功！"
        })


class GetCommentList(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        c_id = req_data['c_id']

        # 检查课程是否存在
        try:
            course = Course.objects.get(id=c_id)
        except Course.DoesNotExist:
            return Response({
                "code": 400,
                "message": "课程不存在"
            }, status=400)

        # 获取课程的所有评论
        comments = Comment.objects.filter(course=course)
        data = []
        for comment in comments:
            data.append({
                "cm_id": comment.id,
                "s_name": comment.student.s_name,
                "s_id": comment.student.s_id,
                "degree": comment.degree,
                "content": comment.content,
                "time": comment.time
            })

        return Response({
            "code": 200,
            "message": "操作成功！",
            "data": data
        })


class DeleteComment(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        s_id = req_data['s_id']
        cm_id = req_data['cm_id']
        try:
            comment = Comment.objects.get(id=cm_id)
        except Comment.DoesNotExist:
            return Response({
                "code": 400,
                "message": "评论不存在"
            })
        if comment.student.s_id == s_id:
            comment.delete()
            return Response({
                "code": 200,
                "message": "操作成功！"
            })
        else:
            return Response({
                "code": 401,
                "error": "不允许删除其他同学的帖子！"
            })


class GetPostThemeList(APIView):
    def get(self, request):
        post_themes = PostTheme.objects.all()
        data = [{
            "pt_id": post_theme.id,
            "s_id": post_theme.student.s_id,
            "s_name": post_theme.student.s_name,
            "title": post_theme.title,
            "content": post_theme.content,
            "time": post_theme.time,
        } for post_theme in post_themes]
        return Response({
            "code": 200,
            "message": "操作成功！",
            "data": data
        })


class BuildPostTheme(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        s_id = req_data['s_id']
        title = req_data['title']
        content = req_data['content']
        time = req_data['time']
        student = Student.objects.get(s_id=s_id)
        post_theme = PostTheme.objects.create(student=student, title=title, content=content, time=time)
        post_theme.save()
        return Response({
            "code": 200,
            "message": "操作成功！"
        })


class GetPostList(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        pt_id = req_data['pt_id']
        posts = Post.objects.filter(post_theme__id=pt_id)
        data = [{
            "p_id": post.id,
            "s_id": post.student.s_id,
            "s_name": post.student.s_name,
            "content": post.content,
            "time": post.time,
        } for post in posts]
        return Response({
            "code": 200,
            "message": "操作成功！",
            "data": data
        })


class BuildPost(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        pt_id = req_data['pt_id']
        s_id = req_data['s_id']
        content = req_data['content']
        time = req_data['time']
        student = Student.objects.get(s_id=s_id)
        post_theme = PostTheme.objects.get(id=pt_id)
        post = Post.objects.create(student=student, post_theme=post_theme, content=content, time=time)
        post.save()
        return Response({
            "code": 200,
            "message": "操作成功！"
        })


class DeletePostTheme(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        pt_id = req_data['pt_id']
        post_theme = PostTheme.objects.get(id=pt_id)
        post_theme.delete()
        return Response({
            "code": 200,
            "message": "操作成功！"
        })


class DeletePost(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        p_id = req_data['p_id']
        post = Post.objects.get(id=p_id)
        post.delete()
        return Response({
            "code": 200,
            "message": "操作成功！"
        })


class GetPostTheme(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        pt_id = req_data['pt_id']
        post_theme = PostTheme.objects.get(id=pt_id)
        data = {
            "pt_id": post_theme.id,
            "s_id": post_theme.student.s_id,
            "s_name": post_theme.student.s_name,
            "title": post_theme.title,
            "content": post_theme.content,
            "time": post_theme.time
        }
        return Response({
            "code": 200,
            "message": "操作成功！",
            "data": data
        })


class GetStudentDiscussNum(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        s_id = req_data['s_id']
        try:
            student = Student.objects.get(s_id=s_id)
        except Student.DoesNotExist:
            return Response({
                "code": 400,
                "error": "学生不存在"
            })
        post_themes = PostTheme.objects.filter(student=student)
        num = len(post_themes)
        return Response({
            "code": 200,
            "message": "操作成功！",
            "data": {
                "discussNum": num
            }
        })


class GetDegree(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        c_id = req_data['c_id']
        course = Course.objects.get(id=c_id)
        sum = 0
        avgDegree = 0
        comment = Comment.objects.filter(course__id=course.id)
        if Comment.objects.filter(course__id=course.id).exists():
            for c in comment:
                sum += int(c.degree)
            avgDegree = sum / len(comment)
        return Response({
            "code": 200,
            "message": "操作成功！",
            "data": {
                "avgDegree": avgDegree
            }
        })


class TeacherChangeInfo(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        t_id = req_data['t_id']
        t_department = req_data['t_department']
        t_email = req_data['t_email']
        t_phone = req_data['t_phone']
        t_office = req_data['t_office']
        try:
            teacher = Teacher.objects.get(t_id=t_id)
        except Teacher.DoesNotExist:
            return Response({
                "code": 404,
                "error": "教师不存在"
            })
        # 更新教师信息
        teacher.t_department = t_department
        teacher.t_email = t_email
        teacher.t_phone = t_phone
        teacher.t_office = t_office
        teacher.save()
        return Response({
            "code": 200,
            "message": "操作成功！"
        })