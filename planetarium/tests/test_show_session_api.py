from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from planetarium.models import ShowSession, AstronomyShow, PlanetariumDome, Ticket
from planetarium.serializers import ShowSessionRetrieveSerializer


def detail_url(show_session_id):
    return reverse("planetarium:show-sessions-detail", args=[show_session_id])


def sample_show_session(**params) -> ShowSession:
    show, _ = AstronomyShow.objects.get_or_create(title="Test Show")
    dome, _ = PlanetariumDome.objects.get_or_create(
        name="Test Dome", rows=5, seats_in_row=10
    )

    defaults = {
        "astronomy_show": show,
        "planetarium_dome": dome,
        "show_time": timezone.now(),
    }
    defaults.update(params)
    return ShowSession.objects.create(**defaults)


def sample_show_session_with_tickets(num_tickets: int = 2) -> ShowSession:
    session = sample_show_session()
    for i in range(num_tickets):
        Ticket.objects.create(
            row=i + 1,
            seat=1,
            show_session=session,
        )
    return session


class UnauthenticatedShowSessionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.show_session_url = reverse("planetarium:show-sessions-list")

    def test_auth_required(self):
        res = self.client.get(self.show_session_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedShowSessionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="testpassword",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)
        self.show_session_url = reverse("planetarium:show-sessions-list")
        self.show = AstronomyShow.objects.create(title="Test Show")
        self.dome = PlanetariumDome.objects.create(
            name="Test Dome", rows=5, seats_in_row=10
        )

    def test_show_session_list(self):
        session = sample_show_session()
        res = self.client.get(self.show_session_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(
            res.data["results"][0]["tickets_available"],
            self.dome.rows * self.dome.seats_in_row,
        )
        self.assertEqual(res.data["results"][0]["astronomy_show"], self.show.title)
        self.assertEqual(res.data["results"][0]["planetarium_dome"], self.dome.name)

    def test_create_show_session_successful(self):
        show_time = timezone.now() + timezone.timedelta(days=1)
        payload = {
            "astronomy_show": self.show.id,
            "planetarium_dome": self.dome.id,
            "show_time": show_time.isoformat(),
        }
        res = self.client.post(self.show_session_url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShowSession.objects.count(), 1)

    def test_create_show_session_unique_constraint(self):
        show_time = timezone.now() + timezone.timedelta(days=2)
        ShowSession.objects.create(
            astronomy_show=self.show, planetarium_dome=self.dome, show_time=show_time
        )
        payload = {
            "astronomy_show": self.show.id,
            "planetarium_dome": self.dome.id,
            "show_time": show_time.isoformat(),
        }
        res = self.client.post(self.show_session_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "The fields planetarium_dome, show_time must make a unique set.",
            str(res.data),
        )

    def test_retrieve_show_session_detail(self):
        session = sample_show_session()
        url = detail_url(session.id)
        res = self.client.get(url)
        serializer = ShowSessionRetrieveSerializer(session)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
