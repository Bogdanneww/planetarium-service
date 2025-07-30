from django.http import JsonResponse
from rest_framework.generics import get_object_or_404

from planetarium.models import PlanetariumDome
from planetarium.serializers import PlanetariumDomeSerializer


def planetarium_dome_list(request):
    if request.method == "GET":
        planetarium_domes = PlanetariumDome.objects.all()
        serializer = PlanetariumDomeSerializer(planetarium_domes, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)


def planetarium_dome_detail(request, pk):
    if request.method == "GET":
        planetarium_dome = get_object_or_404(PlanetariumDome, pk=pk)
        serializer = PlanetariumDomeSerializer(planetarium_dome)
        return JsonResponse(serializer.data, status=200)
