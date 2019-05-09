"""OnlineStudy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from startX.serivce.v1 import site
from LoginAuth import views

urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    path('index/', views.index),
    path('admin/', admin.site.urls),
    path('api/v1/', include(('generic.urls', 'generic'))),  # 主业务
    path('api/v1/auth/', include(('LoginAuth.urls', 'LoginAuth'))),  # 登录认证
    path('api/v1/pay/', include(('Alipay.urls', 'Alipay'))),  # 支付宝支付
    path('blv/', include(('blwvideo.urls', 'blwvideo'))),  # 保利威加密视频接口
    path('backend/', site.urls),  # 后台相关管理
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^account/trend/(?P<year>\d+)/$', views.account_trend, name='account_trend'),
    re_path(r'^order/trend/(?P<year>\d+)/$', views.order_trend, name='order_trend'),
    re_path(r'^rbac/', include(('rbac.urls', 'rbac'))),  # 权限配置

]
