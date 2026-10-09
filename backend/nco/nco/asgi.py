"""
ASGI config for nco project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nco.settings')
django.setup()


from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from apps.report.middleware_stack import JWTAuthMiddlewareStack
import apps.report.routing as report_routing
import apps.lagna.routing as lagna_routing
# import importlib 

application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddlewareStack(
        URLRouter(
            # importlib.import_module('apps.report.routing').websocket_urlpatterns
            report_routing.websocket_urlpatterns + lagna_routing.websocket_urlpatterns
        )
    ),
})


