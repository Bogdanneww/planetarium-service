from django.db.models import Count, F
from rest_framework import viewsets

from planetarium.models import PlanetariumDome, ShowSession, Reservation, AstronomyShow, Ticket, ShowTheme
from planetarium.serializers import PlanetariumDomeSerializer, ShowSessionSerializer, ShowSessionListSerializer, \
    ReservationSerializer, AstronomyShowSerializer, AstronomyShowListSerializer, TicketSerializer, ShowThemeSerializer, \
    AstronomyShowRetrieveSerializer, ShowSessionRetrieveSerializer


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer
        elif self.action == "retrieve":
            return AstronomyShowRetrieveSerializer

        return AstronomyShowSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            return queryset.prefetch_related("themes")

        return queryset


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all().select_related()

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        elif self.action == "retrieve":
            return ShowSessionRetrieveSerializer

        return ShowSessionSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action in "list":
            queryset = (
                queryset
                .select_related("planetarium_dome")
                .annotate(tickets_available=F("planetarium_dome__rows") * F("planetarium_dome__seats_in_row") - Count("tickets"))
            )
        elif self.action in "retrieve":
            queryset = queryset.select_related()

        return queryset
