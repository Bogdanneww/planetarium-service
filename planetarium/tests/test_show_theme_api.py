from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from planetarium.models import ShowTheme
from planetarium.serializers import ShowThemeSerializer


def show_theme_detail_url(theme_id):
    return reverse("planetarium:show-themes-detail", args=[theme_id])


def sample_show_theme(**params):
    defaults = {"name": "Space Travel"}
    defaults.update(params)
    return ShowTheme.objects.create(**defaults)


class UnauthenticatedShowThemeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("planetarium:show-themes-list")

    def test_auth_required(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedShowThemeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="testpass123",
            is_staff=True
        )
        self.client.force_authenticate(self.user)
        self.url = reverse("planetarium:show-themes-list")

    def test_list_show_themes(self):
        sample_show_theme(name="Planets")
        sample_show_theme(name="Stars")

        res = self.client.get(self.url)
        themes = ShowTheme.objects.all()
        serializer = ShowThemeSerializer(themes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_retrieve_show_theme(self):
        theme = sample_show_theme(name="Comets")
        url = show_theme_detail_url(theme.id)

        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], theme.name)

    def test_create_show_theme(self):
        payload = {"name": "Nebulae"}

        res = self.client.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ShowTheme.objects.filter(name=payload["name"]).exists())

    def test_update_show_theme(self):
        theme = sample_show_theme(name="Old Theme")
        payload = {"name": "New Theme"}
        url = show_theme_detail_url(theme.id)

        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        theme.refresh_from_db()
        self.assertEqual(theme.name, payload["name"])

    def test_delete_show_theme(self):
        theme = sample_show_theme(name="To Delete")
        url = show_theme_detail_url(theme.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ShowTheme.objects.filter(id=theme.id).exists())
