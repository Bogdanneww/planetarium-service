from django.urls import path

from planetarium.views import PlanetariumDomeList, PlanetariumDomeDetail


app_name = "planetarium"

urlpatterns = [
    path("planetarium-domes/", PlanetariumDomeList.as_view(), name="planetarium_dome_list"),
    path("planetarium-domes/<int:pk>/", PlanetariumDomeDetail.as_view(), name="planetarium_dome_detail"),
]
