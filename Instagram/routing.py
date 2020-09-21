from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from chat.consumers import ChatConsumer
from .middleware import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddlewareStack(URLRouter([
        path('ws/chat/', ChatConsumer),
    ])),
})
