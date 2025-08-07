from rest_framework import routers
from django.urls import path, include

from planetarium.views import (
    PlanetariumDomeViewSet,
    ShowSessionViewSet,
    TicketViewSet,
    ReservationViewSet,
    AstronomyShowViewSet,
    ShowThemeViewSet,
)

app_name = "planetarium"

router = routers.DefaultRouter()

router.register("planetarium-domes", PlanetariumDomeViewSet, basename="planetarium-domes")
router.register("show-sessions", ShowSessionViewSet, basename="show-sessions")
router.register("reservations", ReservationViewSet, basename="reservations")
router.register("astronomy-shows", AstronomyShowViewSet, basename="astronomy-shows")
router.register("show-themes", ShowThemeViewSet, basename="show-themes")
router.register("tickets", TicketViewSet, basename="tickets")

urlpatterns = [
    path("", include(router.urls)),
]
