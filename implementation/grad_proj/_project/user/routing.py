from django.urls import path

from .consumers import WorkerPageConsumer

websocket_urlpatterns = [
    path('worker_page/<str:id>', WorkerPageConsumer.as_asgi())
]