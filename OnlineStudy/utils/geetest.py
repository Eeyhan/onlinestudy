#!coding:utf-8
import sys
import random
import json
import requests
import time
from hashlib import md5


if sys.version_info >= (3,):
    xrange = range    

VERSION = "3.0.0"


class GeetestLib(object):

    FN_CHALLENGE = "geetest_challenge"
    FN_VALIDATE = "geetest_validate"
    FN_SECCODE = "geetest_seccode"

    GT_STATUS_SESSION_KEY = "gt_server_status"

    API_URL = "http://api.geetest.com"
    REGISTER_HANDLER = "/register.php"
    VALIDATE_HANDLER = "/validate.php"
    JSON_FORMAT = False

    def __init__(self, captcha_id, private_key):
        self.private_key = private_key
        self.captcha_id = captcha_id
        self.sdk_version = VERSION
        self._response_str = ""


    def pre_process(self, user_id=None,new_captcha=1,JSON_FORMAT=1,client_type="web",ip_address=""):
        """
        验证初始化预处理.
        //TO DO  arrage the parameter
        """
        status, challenge = self._register(user_id,new_captcha,JSON_FORMAT,client_type,ip_address)
        self._response_str = self._make_response_format(status, challenge,new_captcha)
        return status

    def _register(self, user_id=None,new_captcha=1,JSON_FORMAT=1,client_type="web",ip_address=""):
        pri_responce = self._register_challenge(user_id,new_captcha,JSON_FORMAT,client_type,ip_address)
        if pri_responce:
            if JSON_FORMAT == 1:
                response_dic = json.loads(pri_responce)
                challenge = response_dic["challenge"]
            else:
                challenge = pri_responce
        else:
            challenge=" "
        if len(challenge) == 32:
            challenge = self._md5_encode("".join([challenge, self.private_key]))
            return 1,challenge
        else:
            return 0, self._make_fail_challenge()

    def get_response_str(self):
        return self._response_str

    def _make_fail_challenge(self):
        rnd1 = random.randint(0, 99)
        rnd2 = random.randint(0, 99)
        md5_str1 = self._md5_encode(str(rnd1))
        md5_str2 = self._md5_encode(str(rnd2))
        challenge = md5_str1 + md5_str2[0:2]
        return challenge

    def _make_response_format(self, success=1, challenge=None,new_captcha=1):
        if not challenge:
            challenge = self._make_fail_challenge()
        if new_captcha:
            string_format = json.dumps(
                {'success': success, 'gt':self.captcha_id, 'challenge': challenge,"new_captcha":True})
        else:
            string_format = json.dumps(
                {'success': success, 'gt':self.captcha_id, 'challenge': challenge,"new_captcha":False})
        return string_format

    def _register_challenge(self, user_id=None,new_captcha=1,JSON_FORMAT=1,client_type="web",ip_address=""):
        if user_id:
            register_url = "{api_url}{handler}?gt={captcha_ID}&user_id={user_id}&json_format={JSON_FORMAT}&client_type={client_type}&ip_address={ip_address}".format(
                    api_url=self.API_URL, handler=self.REGISTER_HANDLER, captcha_ID=self.captcha_id, user_id=user_id,new_captcha=new_captcha,JSON_FORMAT=JSON_FORMAT,client_type=client_type,ip_address=ip_address)
        else:
            register_url = "{api_url}{handler}?gt={captcha_ID}&json_format={JSON_FORMAT}&client_type={client_type}&ip_address={ip_address}".format(
                    api_url=self.API_URL, handler=self.REGISTER_HANDLER, captcha_ID=self.captcha_id,new_captcha=new_captcha,JSON_FORMAT=JSON_FORMAT,client_type=client_type,ip_address=ip_address)
        try:
            response = requests.get(register_url, timeout=2)
            if response.status_code == requests.codes.ok:
                res_string = response.text
            else:
                res_string = ""
        except:
            res_string = ""
        return res_string

    def success_validate(self, challenge, validate, seccode, user_id=None,gt=None,data='',userinfo='',JSON_FORMAT=1):
        """
        正常模式的二次验证方式.向geetest server 请求验证结果.
        """
        if not self._check_para(challenge, validate, seccode):
            return 0
        if not self._check_result(challenge, validate):
            return 0
        validate_url = "{api_url}{handler}".format(
            api_url=self.API_URL, handler=self.VALIDATE_HANDLER)
        query = {
            "seccode": seccode,
            "sdk": ''.join( ["python_",self.sdk_version]),
            "user_id": user_id,
            "data":data,
            "timestamp":time.time(),
            "challenge":challenge,
            "userinfo":userinfo,
            "captchaid":gt,
            "json_format":JSON_FORMAT
        }
        backinfo = self._post_values(validate_url, query)
        if JSON_FORMAT == 1:
            backinfo = json.loads(backinfo)
            backinfo = backinfo["seccode"]
        if backinfo == self._md5_encode(seccode):
            return 1
        else:
            return 0

    def _post_values(self, apiserver, data):
        response = requests.post(apiserver, data)
        return response.text

    def _check_result(self, origin, validate):
        encodeStr = self._md5_encode(self.private_key + "geetest" + origin)
        if validate == encodeStr:
            return True
        else:
            return False

    def failback_validate(self, challenge, validate, seccode):
        """
        failback模式的二次验证方式.在本地对轨迹进行简单的判断返回验证结果.
        """
        if not self._check_para(challenge, validate, seccode):
            return 0
        validate_result = self._failback_check_result(
            challenge, validate,)
        return validate_result

    def _failback_check_result(self,challenge,validate):
        encodeStr = self._md5_encode(challenge)
        if validate == encodeStr:
            return True
        else:
            return False



    def _check_para(self, challenge, validate, seccode):
        return (bool(challenge.strip()) and bool(validate.strip()) and  bool(seccode.strip()))



    def _md5_encode(self, values):
        if type(values) == str:
            values = values.encode()
        m = md5(values)
        return m.hexdigest()

