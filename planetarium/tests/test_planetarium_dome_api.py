from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from planetarium.models import PlanetariumDome
from planetarium.serializers import PlanetariumDomeSerializer


def detail_url(planetarium_dome_id):
    return reverse("planetarium:planetarium-domes-detail", args=[planetarium_dome_id])


def sample_planetarium_dome(**params) -> PlanetariumDome:
    defaults = {"name": "Testdome", "rows": 10, "seats_in_row": 10}
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
            email="test@test.test", password="testpassword"
        )
        self.client.force_authenticate(self.user)
        self.planetarium_dome_url = reverse("planetarium:planetarium-domes-list")

    def test_planetarium_domes_list(self):
        sample_planetarium_dome()
        res = self.client.get(self.planetarium_dome_url)
        domes = PlanetariumDome.objects.all()
        serializer = PlanetariumDomeSerializer(domes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_create_dome_forbidden(self):
        payload = {"name": "ForbiddenDome", "rows": 5, "seats_in_row": 5}
        res = self.client.post(self.planetarium_dome_url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(PlanetariumDome.objects.count(), 0)


class AdminPlanetariumDomeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = get_user_model().objects.create_user(
            email="admin@test.test",
            password="testpassword",
            is_staff=True,
        )
        self.client.force_authenticate(self.admin_user)
        self.planetarium_dome_url = reverse("planetarium:planetarium-domes-list")

    def test_create_dome_successful(self):
        payload = {"name": "NewDome", "rows": 20, "seats_in_row": 25}
        res = self.client.post(self.planetarium_dome_url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PlanetariumDome.objects.count(), 1)
        dome = PlanetariumDome.objects.first()
        for key, value in payload.items():
            self.assertEqual(getattr(dome, key), value)

    def test_update_dome_successful(self):
        dome = sample_planetarium_dome()
        url = detail_url(dome.id)
        payload = {"name": "UpdatedDome", "rows": 15, "seats_in_row": 15}
        res = self.client.put(url, payload)

        dome.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(dome.name, payload["name"])
        self.assertEqual(dome.rows, payload["rows"])
        self.assertEqual(dome.seats_in_row, payload["seats_in_row"])

    def test_delete_dome_successful(self):
        dome = sample_planetarium_dome()
        url = detail_url(dome.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PlanetariumDome.objects.filter(id=dome.id).exists())
