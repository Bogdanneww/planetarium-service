from rest_framework import routers
from django.urls import path, include

from planetarium.views import PlanetariumDomeViewSet


app_name = "planetarium"

router = routers.DefaultRouter()

router.register("planetarium-domes", PlanetariumDomeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
