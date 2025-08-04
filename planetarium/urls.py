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

router.register("planetarium-domes", PlanetariumDomeViewSet)
router.register("show-sessions", ShowSessionViewSet)
router.register("reservations", ReservationViewSet)
router.register("astronomy-shows", AstronomyShowViewSet)
router.register("show-themes", ShowThemeViewSet)
router.register("tickets", TicketViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
