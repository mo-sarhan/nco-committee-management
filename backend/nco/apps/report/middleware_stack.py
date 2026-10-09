from channels.middleware import BaseMiddleware
from .middleware import JWTAuthMiddleware
import django.contrib.sessions

def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(inner)