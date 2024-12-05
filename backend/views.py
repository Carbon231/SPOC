import json
from django.utils.deprecation import MiddlewareMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.models import Student, Teacher


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
            return Response({
                "code": 200,
                "message": "登录成功"
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
        user = Teacher.objects.create(t_id=t_id, t_name=t_name, t_pwd=t_pwd)
        user.save()
        return Response({
            "code": 200,
            "message": "注册成功"
        })