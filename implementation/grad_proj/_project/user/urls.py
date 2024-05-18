from django.urls import path
from . import views
from user.consumers import WorkerPageConsumer  


urlpatterns = [
    path('',views.login, name='login' ),
    path('home',views.home, name='home' ),
    path('supervisor_login',views.supervisor_login, name='supervisor_login' ),
    path('manager',views.manager, name='manager' ),
    path('supervisor/<str:id>',views.supervisor, name='supervisor' ),
    path('ws/worker_page/<str:id>', WorkerPageConsumer.as_asgi()),
    path('sites',views.sites, name='sites' ),
    path('helmets',views.helmets, name='helmets' ),
    path('reports',views.reports, name='reports' ),
    path('workers',views.workers, name='workers' ),
    path('supervisors',views.supervisors, name='supervisors' ),
    path('organization',views.organization, name='organization' ),
    path('supervisor_delete/<str:id>', views.supervisor_delete, name='supervisor_delete'),
    path('site_delete/<str:id>', views.site_delete, name='site_delete'),
    path('worker_delete/<str:id>', views.worker_delete, name='worker_delete'),
    path('helmet_delete/<str:id>', views.helmet_delete, name='helmet_delete'),
]
# websocket_urlpatterns = [
#     path('worker_page/<str:id>', WorkerPageConsumer.as_asgi()),
# ]