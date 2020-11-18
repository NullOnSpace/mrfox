## Issues

### Zombie `channel_layer`
When a ws close unexpectly, the `disconnect` method wont be called. Thus there will be a zombie channel in backends group, which will slow down the group send apparently.

#### Solution
In AppConfig.ready, remove all the "asgi:group:*" keys in redis backend.
But in uwsgi, the harikiri will kill instance and restart it, the cleaning up will influence other instances.
