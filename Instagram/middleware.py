from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token

User = get_user_model()


@database_sync_to_async
def get_user(access_token):
    try:
        return Token.objects.get(key=access_token).user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        query_string = parse_qs(self.scope['query_string'].decode())
        token = query_string.get('token')
        if not token:
            self.scope['user'] = AnonymousUser()
            inner = self.inner(self.scope)
            return await inner(receive, send)
        access_token = token[0]
        user = await get_user(access_token)
        if not user.is_active:
            self.scope['user'] = AnonymousUser()
            inner = self.inner(self.scope)
            return await inner(receive, send)
        self.scope['user'] = user
        inner = self.inner(self.scope)
        return await inner(receive, send)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
