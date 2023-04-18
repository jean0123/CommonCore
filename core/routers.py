from django.urls import path, include
from lists.urls import router as list_router
from users.urls import router as user_router

drf_url = [
    path('users/', include(user_router.urls)),
    path('lists/', include(list_router.urls)),
]