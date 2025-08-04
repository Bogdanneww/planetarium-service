from django.db.models import Count, F
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from planetarium.models import (
    PlanetariumDome,
    ShowSession,
    Reservation,
    AstronomyShow,
    Ticket,
    ShowTheme,
)
from planetarium.permissions import IsAdminAllOrIsAuthenticate
from planetarium.serializers import (
    PlanetariumDomeSerializer,
    ShowSessionSerializer,
    ShowSessionListSerializer,
    ReservationSerializer,
    AstronomyShowSerializer,
    AstronomyShowListSerializer,
    TicketSerializer,
    ShowThemeSerializer,
    AstronomyShowRetrieveSerializer,
    ShowSessionRetrieveSerializer,
    ReservationListSerializer,
    PlanetariumDomeImageSerializer,
)


@extend_schema_view(
    create=extend_schema(
        request=PlanetariumDomeSerializer,
        responses=PlanetariumDomeSerializer,
        description="Create a new planetarium dome.",
    ),
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "themes",
                type={"type": "array", "items": {"type": "number"}},
                description="Show themes",
                location=OpenApiParameter.QUERY,
                style="form",
                explode=True,
            )
        ]
    ),
)
class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PlanetariumDomeSerializer
        elif self.action == "retrieve":
            return PlanetariumDomeSerializer
        elif self.action == "upload_image":
            return PlanetariumDomeImageSerializer
        return PlanetariumDomeSerializer

    @action(
        methods=["post"],
        detail=True,
        url_path="upload-image",
    )
    def upload_image(self, request):
        planetarium_dome = self.get_object()
        serializer = self.get_serializer(
            planetarium_dome,
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    create=extend_schema(
        request=ReservationSerializer,
        responses=ReservationSerializer,
        description="Create a new reservation with tickets",
    )
)
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if self.action == "list":
            queryset = queryset.prefetch_related(
                "tickets__show_session__planetarium_dome"
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        serializer = self.serializer_class

        if self.action == "list":
            serializer = ReservationListSerializer

        return serializer


@extend_schema_view(
    create=extend_schema(
        request=AstronomyShowSerializer,
        responses=AstronomyShowSerializer,
        description="Create a new Astronomy Show",
    )
)
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


@extend_schema_view(
    create=extend_schema(
        request=TicketSerializer,
        responses=TicketSerializer,
        description="Create a new ticket",
    )
)
class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


@extend_schema_view(
    create=extend_schema(
        request=ShowThemeSerializer,
        responses=ShowThemeSerializer,
        description="Create a new show theme",
    )
)
class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminAllOrIsAuthenticate,)


@extend_schema_view(
    create=extend_schema(
        request=ShowSessionSerializer,
        responses=ShowSessionSerializer,
        description="Create a new show session",
    )
)
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
            queryset = queryset.select_related("planetarium_dome").annotate(
                tickets_available=F("planetarium_dome__rows")
                * F("planetarium_dome__seats_in_row")
                - Count("tickets")
            )
        elif self.action in "retrieve":
            queryset = queryset.select_related()

        return queryset.order_by("id")
