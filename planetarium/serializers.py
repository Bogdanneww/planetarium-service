from rest_framework import serializers
from planetarium.models import PlanetariumDome, ShowSession, Reservation, AstronomyShow, Ticket, ShowTheme


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = "__all__"


class PlanetariumDomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanetariumDome
        fields = "__all__"


class ShowSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowSession
        fields = "__all__"


class ShowSessionListSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.CharField(source="astronomy_show.title", read_only=True)
    planetarium_dome = serializers.CharField(source="planetarium_dome.name", read_only=True)

    class Meta:
        model = ShowSession
        fields = "__all__"


class ShowSessionRetrieveSerializer(ShowSessionSerializer):
    planetarium_dome = PlanetariumDomeSerializer(many=True, read_only=True)


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = "__all__"


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
