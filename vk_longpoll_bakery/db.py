import os

import redis
from dotenv import load_dotenv


load_dotenv()


class RedisSingleton:
    _instance = None

    @staticmethod
    def get_connection():
        if not RedisSingleton._instance:
            RedisSingleton._instance = redis.Redis(
                host=os.getenv('REDIS_HOST'),
                port=os.getenv('REDIS_PORT'),
                db=0
            )
        return RedisSingleton._instance
