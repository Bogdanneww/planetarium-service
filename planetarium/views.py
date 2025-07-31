from rest_framework import viewsets

from planetarium.models import PlanetariumDome
from planetarium.serializers import PlanetariumDomeSerializer


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
