from rest_framework import serializers
from planetarium.models import PlanetariumDome


class PlanetariumDomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanetariumDome
        fields = "__all__"
