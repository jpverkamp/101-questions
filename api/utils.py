import redis as redislib

def redis():
    return redislib.StrictRedis(host = 'redis', decode_responses = True)
