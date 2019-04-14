# coding:utf-8

from rest_framework.views import APIView
from rest_framework.response import Response
from utils.geetest import GeetestLib
from django.shortcuts import HttpResponse
from utils.redis_pool import POOL
from utils.BaseResponse import BaseResponse
from LoginAuth.serializers import RegisterSerializer
from generic.views import ShoppingView
from generic.models import Account
from utils.Auther import Auther
import redis
import json
import uuid

pc_geetest_id = "64936e8e1ad53dad8bbee6f96224e7d0"
pc_geetest_key = "8322ed330d370a704a77d8205c94d20f"

# pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
# pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"

RedisConn = redis.Redis(connection_pool=POOL)


class IndexView(APIView):
    authentication_classes = [Auther, ]

    def get(self, request):
        return Response('首页，欢迎%s' % request.user.username)


class RegisterView(APIView):
    """注册"""

    def post(self, request):
        res = BaseResponse()
        user_obj = RegisterSerializer(data=request.data)
        if user_obj.is_valid():
            user_obj.save()
            res.data = user_obj.data
        else:
            res.code = 1020
            res.error = user_obj.errors
        return Response(res.dict)


class LoginView(APIView):
    """登录"""

    def post(self, request):
        res = BaseResponse()
        username = request.data.get('username')
        passwd = request.data.get('passwd')
        user_obj = Account.objects.filter(username=username, passwd=passwd).first()
        if not user_obj:
            res.code = 1030
            res.error = '用户名密码不匹配'
        try:
            token = uuid.uuid4()
            RedisConn.set(str(token), user_obj.id)
            shop_cart = ShoppingView().get(request)  # 购物车数据
            print(shop_cart.data)
            res.data = {
                'access_token': token,
                'avatar': 'http://127.0.0.1:8000/media/avatar.png',  # 真实部署时改成公网地址
                'username': user_obj.username,
                'shop_cart_num': shop_cart.data.get('data')
            }
            # 头像，购物车数据，token,用户名
        except Exception as e:
            print('........', e)
            res.code = 1031
            res.error = '创建令牌失败'
        return Response(res.dict)


class LoginAuthView(APIView):
    def get(self, request):
        user_id = 'Auth_'
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        status = gt.pre_process(user_id)
        # request.session[gt.GT_STATUS_SESSION_KEY] = status
        # request.session["user_id"] = user_id
        RedisConn.set(gt.GT_STATUS_SESSION_KEY, status)
        RedisConn.set("user_id", user_id)
        response_str = gt.get_response_str()
        return HttpResponse(response_str)

    def post(self, request):
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.data.get(gt.FN_CHALLENGE, '')
        validate = request.data.get(gt.FN_VALIDATE, '')
        seccode = request.data.get(gt.FN_SECCODE, '')
        # status = request.session[gt.GT_STATUS_SESSION_KEY]
        # user_id = request.session["user_id"]
        status = RedisConn.get(gt.GT_STATUS_SESSION_KEY)
        user_id = RedisConn.get("user_id")
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}
        print(request.data)
        return HttpResponse(json.dumps(result))
