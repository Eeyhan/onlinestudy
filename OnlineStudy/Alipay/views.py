#!/usr/bin/env python
# -*- coding: utf-8 -*-
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect, HttpResponse
from utils.BaseResponse import BaseResponse


def alipayclient():
    """
    设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
    """
    alipay_client_config = AlipayClientConfig(sandbox_debug=True)
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '2016092700611690'
    with open("Alipay/keys/private_key.txt") as f:
        alipay_client_config.app_private_key = f.read()
    # 阿里的公钥
    with open("Alipay/keys/public_key.txt") as f:
        alipay_client_config.alipay_public_key = f.read()

    """
    得到客户端对象。
    注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
    logger参数用于打印日志，不传则不打印，建议传递。
    """
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config)
    return client


"""
系统接口示例：alipay.trade.pay
"""


class AlipayView(APIView):
    def get(self, request):
        return render(request, 'pay.html')

    def post(self, request):
        money = request.data.get('money')
        try:
            if isinstance(money, str):
                money = float('%.2f' % float(money))

        except Exception as e:
            print(e)
            return Response('错误，只能是数字')

        client = alipayclient()

        """
        页面接口示例：alipay.trade.page.pay
        """
        # 对照接口文档，构造请求对象
        model = AlipayTradePagePayModel()
        import time
        model.out_trade_no = 'pay' + str(time.time())
        model.total_amount = money
        model.subject = "测试"
        model.body = "支付宝测试"
        model.product_code = "FAST_INSTANT_TRADE_PAY"
        request = AlipayTradePagePayRequest(biz_model=model)
        # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段

        # get请求 用户支付成功后返回的页面请求地址
        # request.return_url = "http://127.0.0.1:8000/api/v1/pay/alipay_handler"
        request.return_url = "http://localhost:8080/Order"

        # post请求 用户支付成功通知商户的请求地址
        # request.notify_url = "http://127.0.0.1:8000/api/v1/pay/alipay_handler"

        request.notify_url = "http://127.0.0.1:8000/api/v1/pay/alipay_handler"
        response = client.page_execute(request, http_method="GET")
        print("alipay.trade.page.pay response:" + response)
        # return redirect(response)
        return HttpResponse(response)


class PayHandlerView(APIView):
    def get(self, request):
        # return_url的回调地址
        print('get', request.data)
        # 用户支付成功之后回到哪
        return HttpResponse("用户支付成功")

    def post(self, request):
        print('post0', request.data)
        return HttpResponse("notify_url")
