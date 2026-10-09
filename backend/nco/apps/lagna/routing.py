from django.urls import re_path
from .consumers import LagnaShowConsumer



websocket_urlpatterns = [
    re_path('ws/lagna/$',LagnaShowConsumer.as_asgi())
]
