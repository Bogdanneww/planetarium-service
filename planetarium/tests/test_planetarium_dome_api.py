from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from planetarium.models import PlanetariumDome
from planetarium.serializers import PlanetariumDomeSerializer


def detail_url(planetarium_dome_id):
    return reverse("planetarium-domes-detail", args=[planetarium_dome_id])


def sample_planetarium_dome(**params) -> PlanetariumDome:
    defaults = {
        "name": "Testname",
        "rows": "10",
        "seats_in_row": "10"
    }
    defaults.update(params)
    return PlanetariumDome.objects.create(**defaults)


class UnauthenticatedPlanetariumDomeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.planetarium_dome_url = reverse("planetarium:planetarium-domes-list")

    def test_auth_required(self):
        res = self.client.get(self.planetarium_dome_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlanetariumDomeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="testpassword"
        )
        self.client.force_authenticate(self.user)
        self.planetarium_dome_url = reverse("planetarium:planetarium-domes-list")

    def test_planetarium_domes_list(self):
        sample_planetarium_dome()
        res = self.client.get(self.planetarium_dome_url)
        domes = PlanetariumDome.objects.all()
        serializer = PlanetariumDomeSerializer(domes, many=True)

        self.assertEqual(res.data["results"], serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
