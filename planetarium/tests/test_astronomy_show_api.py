from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from planetarium.models import AstronomyShow, ShowTheme
from planetarium.serializers import (
    AstronomyShowListSerializer,
    AstronomyShowRetrieveSerializer,
)


def sample_show_theme(name="Space"):
    return ShowTheme.objects.create(name=name)


def sample_astronomy_show(**params):
    defaults = {
        "title": "Black Holes",
        "description": "A deep dive into the mystery of black holes.",
    }
    defaults.update(params)
    show = AstronomyShow.objects.create(
        title=defaults["title"], description=defaults["description"]
    )
    if "themes" in params:
        show.themes.set(params["themes"])
    return show


def detail_url(show_id):
    return reverse("planetarium:astronomy-shows-detail", args=[show_id])


class UnauthenticatedAstronomyShowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("planetarium:astronomy-shows-list")

    def test_auth_required(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAstronomyShowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="password123", is_staff=True
        )
        self.client.force_authenticate(self.user)
        self.url = reverse("planetarium:astronomy-shows-list")

    def test_list_astronomy_shows(self):
        theme = sample_show_theme()
        sample_astronomy_show(themes=[theme])
        res = self.client.get(self.url)

        shows = AstronomyShow.objects.all().prefetch_related("themes")
        serializer = AstronomyShowListSerializer(shows, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_retrieve_astronomy_show(self):
        theme = sample_show_theme()
        show = sample_astronomy_show(themes=[theme])
        res = self.client.get(detail_url(show.id))

        serializer = AstronomyShowRetrieveSerializer(show)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_astronomy_show(self):
        theme = sample_show_theme()
        payload = {
            "title": "Solar Flares",
            "description": "Eruptions from the sun.",
            "themes": [theme.id],
        }
        res = self.client.post(self.url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        show = AstronomyShow.objects.get(id=res.data["id"])
        self.assertEqual(show.title, payload["title"])
        self.assertEqual(show.description, payload["description"])
        self.assertEqual(list(show.themes.all()), [theme])

    def test_update_astronomy_show(self):
        theme1 = sample_show_theme("Cosmos")
        theme2 = sample_show_theme("Nebulae")
        show = sample_astronomy_show(themes=[theme1])

        payload = {
            "title": "Updated Title",
            "description": "Updated Description",
            "themes": [theme2.id],
        }
        res = self.client.put(detail_url(show.id), payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        show.refresh_from_db()
        self.assertEqual(show.title, payload["title"])
        self.assertEqual(show.description, payload["description"])
        self.assertEqual(list(show.themes.all()), [theme2])

    def test_delete_astronomy_show(self):
        show = sample_astronomy_show()
        res = self.client.delete(detail_url(show.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AstronomyShow.objects.filter(id=show.id).exists())
