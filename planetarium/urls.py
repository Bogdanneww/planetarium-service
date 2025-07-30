from django.urls import path

from planetarium.views import planetarium_dome_list, planetarium_dome_detail


app_name = "planetarium"

urlpatterns = [
    path("planetarium-domes/", planetarium_dome_list, name="planetarium_dome_list"),
    path("planetarium-domes/<int:pk>/", planetarium_dome_detail, name="planetarium_dome_detail"),
]
