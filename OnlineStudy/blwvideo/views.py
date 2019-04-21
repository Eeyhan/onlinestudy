from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from utils.polyv import polyv_video
import json


class Polyv(APIView):

    def post(self, request):
        vid = request.data.get("vid")
        remote_addr = request.META.get("REMOTE_ADDR")
        user_id = 1
        user_name = "test"
        verify_data = polyv_video.get_video_token(vid, remote_addr, user_id, user_name)
        return Response(verify_data["token"])

    def get(self, request, *args, **kwargs):
        vid = request.query_params.get("vid", "")
        code = request.query_params.get("code", "")
        t = request.query_params.get("t", "")
        callback = request.query_params.get("callback", "")
        user_name = "test|1234565"
        status = 1
        # username, code, status, t
        sign = polyv_video.get_play_key(vid, user_name, code, status, t)
        print(sign)
        res_str = polyv_video.get_resp(int(status), user_name, sign)
        res_str = json.dumps(res_str, ensure_ascii=False)
        if callback != "":
            ret = callback + "(" + res_str + ")"
        else:
            ret = res_str
        print(ret)
        return HttpResponse(ret)


# 解决跨域
def test_bolyv(request):
    return render(request, "bolyv_test.html")