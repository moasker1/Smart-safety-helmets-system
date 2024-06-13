from django.urls import re_path
from user.consumers import WorkerConsumer

websocket_urlpatterns = [
    re_path(r'ws/worker_page/(?P<worker_id>\w+)/$', WorkerConsumer.as_asgi()),
    # re_path('ws/worker_page/<str:id>/', WorkerPageConsumer.as_asgi()),
]
