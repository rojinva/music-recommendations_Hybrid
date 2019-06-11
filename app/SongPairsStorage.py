import redis

class SongPairsStorage:
  redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
