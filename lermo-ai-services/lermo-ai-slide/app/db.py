import os
import redis

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_INSTANCE = None

def init_redis():
    global REDIS_INSTANCE
    if not REDIS_INSTANCE:
      print("Redis initialized")
      REDIS_INSTANCE = redis.Redis(host=REDIS_HOST, port=6379, db=0)
      response = REDIS_INSTANCE.ping()
      if response:
          print("Redis connection successful")
      else:
          print("Redis connection failed")

def set(key, value):
    REDIS_INSTANCE.set(key, value)

def get(key):
    return REDIS_INSTANCE.get(key)

# def get_all():
#     keys = REDIS_INSTANCE.keys("*")
#     values = REDIS_INSTANCE.mget(keys)
#     return dict(zip(keys, values))

def get_all():
    keys = REDIS_INSTANCE.keys("*")
    values = REDIS_INSTANCE.mget(keys)
    result_dict = dict(zip(keys, values))
    return str(result_dict)

def flushdb_all():
    REDIS_INSTANCE.flushdb()