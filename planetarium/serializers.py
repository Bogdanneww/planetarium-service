from django.db import transaction
from rest_framework import serializers

from planetarium.models import PlanetariumDome, ShowSession, Reservation, AstronomyShow, Ticket, ShowTheme


class ShowThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowTheme
        fields = "__all__"


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    show_themes = serializers.SerializerMethodField()

    class Meta:
        model = PlanetariumDome
        fields = ["id", "name", "rows", "seats_in_row", "total_seats", "show_themes"]

    def get_show_themes(self, dome: PlanetariumDome) -> list[str]:
        themes = ShowTheme.objects.filter(
            shows__showsession__planetarium_dome=dome
        ).distinct()
        return [theme.name for theme in themes]


class AstronomyShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = AstronomyShow
        fields = "__all__"


class AstronomyShowListSerializer(AstronomyShowSerializer):
    themes = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")


class AstronomyShowRetrieveSerializer(AstronomyShowSerializer):
    themes = ShowThemeSerializer(many=True)


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = "__all__"

    def validate(self, attrs):
        show_session = attrs.get("show_session")
        row = attrs.get("row")
        seat = attrs.get("seat")

        if not show_session:
            raise serializers.ValidationError("Show session is required.")

        dome = show_session.planetarium_dome

        if not (1 <= row <= dome.rows):
            raise serializers.ValidationError(f"Invalid row number {row}. Max rows: {dome.rows}.")

        if not (1 <= seat <= dome.seats_in_row):
            raise serializers.ValidationError(f"Invalid seat number {seat}. Max seats per row: {dome.seats_in_row}.")

        return attrs


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ["id", "created_at", "tickets"]

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
            return reservation


class ShowSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowSession
        fields = "__all__"


class ShowSessionListSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.CharField(source="astronomy_show.title", read_only=True)
    planetarium_dome = serializers.CharField(source="planetarium_dome.name", read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time", "tickets_available")


class ShowSessionRetrieveSerializer(ShowSessionSerializer):
    planetarium_dome = PlanetariumDomeSerializer(read_only=True)
    ticket_set = TicketSerializer(many=True, read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time", "ticket_set", "tickets_available")
