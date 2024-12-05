import json
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.models import Student, Teacher


class StudentLogin(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        s_name = req_data['s_name']
        s_pwd = req_data['s_pwd']
        user = Student.objects.get(s_name=s_name)
        if user.s_pwd == s_pwd:
            return Response({
                "code": 200,
                "message": "登录成功"
            })
        else:
            return Response({
                "code": 400,
                "message": "用户名或密码错误"
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
            return Response({
                "code": 200,
                "message": "登录成功"
            })
        else:
            return Response({
                "code": 400,
                "message": "用户名或密码错误"
            })

class TeacherRegister(APIView):
    def post(self, request):
        req_data = json.loads(request.body)
        t_name = req_data['t_name']
        t_pwd = req_data['t_pwd']
        t_id = req_data['t_id']
        user = Teacher.objects.create(t_id=t_id, t_name=t_name, t_pwd=t_pwd)
        user.save()
        return Response({
            "code": 200,
            "message": "注册成功"
        })