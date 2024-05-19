from django.urls import path
from .consumers import WorkerPageConsumer

websocket_urlpatterns = [
    path('ws/worker_page/<str:id>/', WorkerPageConsumer.as_asgi()),
]
