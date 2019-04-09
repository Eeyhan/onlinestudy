import redis

POOL = redis.ConnectionPool(host='127.0.0.1',decode_responses=True,max_connections=20)