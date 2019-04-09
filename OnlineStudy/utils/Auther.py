from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from generic.models import Account
from utils.redis_pool import POOL
import redis

RedisConn = redis.Redis(connection_pool=POOL)


class Auther(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHENTICATION', '')
        if not token:
            return AuthenticationFailed('没有携带token')

        user_id = RedisConn.get(str(token))
        user_obj = Account.objects.filter(id=user_id).first()
        if not user_obj:
            return AuthenticationFailed('非法用户，无效的token')
        return user_obj, token
