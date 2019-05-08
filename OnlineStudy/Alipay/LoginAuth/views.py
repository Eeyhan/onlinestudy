#! /usr/bin/env python
# -*- coding:utf-8 -*-


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
import hashlib
from django.shortcuts import redirect, render
from generic.models import Account
from utils.md5 import gen_md5
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# from rbac.service.init_permission import init_permission


pc_geetest_id = "64936e8e1ad53dad8bbee6f96224e7d0"
pc_geetest_key = "8322ed330d370a704a77d8205c94d20f"

RedisConn = redis.Redis(connection_pool=POOL)


class IndexView(APIView):
    """这是后端测试的接口"""
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
        # 密码加盐
        hash_key = 'password'
        passwd = passwd + hash_key
        passwd_md5 = hashlib.md5(passwd.encode()).hexdigest()
        user_obj = Account.objects.filter(username=username, passwd=passwd_md5).first()
        if not user_obj:
            res.code = 1030
            res.error = '用户名密码不匹配'
        try:
            token = uuid.uuid4()
            RedisConn.set(str(token), user_obj.id)
            shop_cart = ShoppingView().get(request)  # 购物车数据
            res.data = {
                'access_token': token,
                'avatar': 'http://127.0.0.1:8000/media/avatar.png',  # 真实部署时改成公网地址
                'username': user_obj.username,
                'shop_cart_num': shop_cart.data.get('data'),
                'balance': user_obj.balance
            }
            # 头像，购物车数据，token,用户名,账户余额
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

        return HttpResponse(json.dumps(result))


# ################## 后台登录部分 #######################


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    username = request.POST.get('username')
    password = gen_md5(request.POST.get('password'))
    current_user = Account.objects.filter(username=username, passwd=password).first()

    if not current_user:
        return render(request, 'login.html', {'error': '用户名或密码错误'})

    request.session['userinfo'] = {'id': current_user.id, 'username': current_user.username}
    # 用户权限信息的初始化
    # init_permission(current_user, request)

    return redirect('/index/')


def logout(request):
    request.session.delete()
    return redirect('/login/')


def index(request):
    return render(request, 'backend_index.html')


# def test(request):
#     # fig = plt.figure()
#     plt.plot([1, 2, 3, 4], [10, 20, 25, 30], color='lightblue', linewidth=3)
#     plt.xlim(0.5, 4.5)
#     buffer = BytesIO()
#     plt.savefig(buffer)
#     plot_data = buffer.getvalue()
#     imb = base64.b64encode(plot_data)  # 对plot_data进行编码
#     ims = imb.decode()
#     imd = "data:image/png;base64," + ims
#     return render(request, "test.html", {"img": imd})


def test(request):
    from django.http import HttpResponse
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.dates import DateFormatter
    import matplotlib.pyplot as plt
    import datetime, random
    fig = Figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    x = []
    y = []
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now += delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas = FigureCanvasAgg(fig)
    # 方法一：

    # response = HttpResponse(content_type='image/jpg')
    # canvas.print_jpg(response)
    # plt.close(fig)
    # return response

    # 方法二：

    response = HttpResponse(content_type='image/jpeg')
    canvas.print_jpeg(response)
    plt.close(fig)
    return response
