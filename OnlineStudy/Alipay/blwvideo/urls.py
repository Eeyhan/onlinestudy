
from django.urls import path, re_path
from blwvideo.views import test_bolyv
from blwvideo.views import Polyv

urlpatterns = [
    path('polyv', Polyv.as_view()),  # 这里要与客户端url对应，最后有没有【/】要统一
    re_path(r'^crossdomain.xml', test_bolyv)
]