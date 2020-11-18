from django.apps import AppConfig
import redis


class ChatConfig(AppConfig):
    name = 'chat'

    def ready(self):
        print("")
        r = redis.StrictRedis()
        keys = r.keys("asgi:group:*")
        for k in keys:
            r.delete(k)
        keys = r.keys("asgispecific.*")
        for k in keys:
            r.delete(k)
