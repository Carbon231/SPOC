import json
from django.utils.deprecation import MiddlewareMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.models import Student, Teacher, Course, Comment, SC


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
                "message": "学号不存在",
                "error_response": error_response
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
                    "message": "密码错误"
                })



class StudentRegister(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        s_name = req_data['s_name']
        s_pwd = req_data['s_pwd']
        s_id = req_data['s_id']
        user = Student.objects.create(s_id=s_id, s_name=s_name, s_pwd=s_pwd)
        user.save()
        return Response({
            "code": 200,
            "message": "注册成功"
        })

class TeacherLogin(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        t_name = req_data['t_name']
        t_pwd = req_data['s_pwd']
        user = Teacher.objects.get(t_name=t_name)
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
                "message": "用户名或密码错误"
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
                "message": "密码不一致"
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
        s_id = req_data['t_id']
        s_pwd = req_data['t_pwd']
        new_pwd_1 = req_data['new_pwd_1']
        new_pwd_2 = req_data['new_pwd_2']
        try:
            user = Teacher.objects.get(s_id=s_id)
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
            "data": {"num": num}
        })


class GetStudentCommentNum(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        s_id = req_data['s_id']
        comments = Comment.objects.filter(student__id=s_id)
        num = len(comments)
        return Response({
            "code": 200,
            "message": "操作成功！",
            "data": {"num": num}
        })


class GetStudentCourseNum(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        s_id = req_data['s_id']
        scs = SC.objects.filter(student__id=s_id)
        num = len(scs)
        return Response({
            "code": 200,
            "message": "操作成功！",
            "data": {"num": num}
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
            comment = Comment.objects.filter(course__id=course.id)
            for c in comment:
                sum += c.degree
            avgDegree = sum / len(comment)
            data.append({
                "c_id": course.c_id,
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
        course = Course.objects.get(c_id=c_id)
        if SC.objects.filter(student=student, course=course):
            return Response({
                "code": 200,
                "message": "已经选课"
            })
        else:
            SC.objects.create(student=student, course=course)
            return Response({
                "code": 401,
                "message": "操作成功"
            })


class DropCourse(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        c_id = req_data['c_id']
        s_id = req_data['s_id']
        student = Student.objects.get(s_id=s_id)
        course = Course.objects.get(c_id=c_id)
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
        scs = SC.objects.filter(student__id=s_id)
        data = []
        for sc in scs:
            course = sc.course
            sum = 0
            comment = Comment.objects.filter(course__id=course.id)()
            for c in comment:
                sum += c.degree
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


class GetTeacherCourseList(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        t_id = req_data['t_id']
        courses = Course.objects.filter(teacher__t_id=t_id)
        data = []
        for course in courses:
            sum = 0
            comment = Comment.objects.filter(course__id=course.id)()
            for c in comment:
                sum += c.degree
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
                "cm_id": comment.cm_id,
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