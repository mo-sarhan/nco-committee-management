from django.urls import re_path
from .consumers import PrntPhotoReportConsumer



websocket_urlpatterns = [
    re_path('wss/photo/report/$',PrntPhotoReportConsumer.as_asgi())
]
