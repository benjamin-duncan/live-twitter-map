from django.urls import path

from .views import map, health, startup


urlpatterns = [
    path("", map, name="index"),
    path("health/", health, name="health"),
    path("startup/", startup),
]
