from django.urls import path

from core import views # pyright: reportMissingImports=false

urlpatterns = [
    # Template of frontend.
    # Can be used to manually test Websocket connection in browser
    path("api", views.map, name="map"), 

    path("health/", views.health, name="health"),
    path("api/startup/", views.startup, name="startup"),
    path("api/stats/", views.stats, name="stats"),
    path("api/graph/", views.graph, name="graph"),
]
