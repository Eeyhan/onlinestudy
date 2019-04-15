from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from generic.models import Account
from utils.redis_pool import POOL
import redis

RedisConn = redis.Redis(connection_pool=POOL)


class Auther(BaseAuthentication):
    def authenticate(self, request):
        # 前端axios加了请求拦截器之后，会请求两次，第一次OPTIONS，第二次才是真实的数据
        # 并且第一次请求时不带header，所以会报错
        if request.method == 'OPTIONS':
            return
        else:
            token = request.META.get('HTTP_AUTHORIZATION', '')
            if not token:
                return AuthenticationFailed('没有携带token')

            user_id = RedisConn.get(str(token))
            user_obj = Account.objects.filter(id=user_id).first()
            if not user_obj:
                return AuthenticationFailed('非法用户，无效的token')

            return user_obj, token
