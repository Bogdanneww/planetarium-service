from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone

from planetarium.models import (
    Ticket,
    ShowSession,
    PlanetariumDome,
    Reservation,
    AstronomyShow,
)

User = get_user_model()


def sample_dome(**params):
    defaults = {
        "name": "Test Dome",
        "rows": 10,
        "seats_in_row": 12,
    }
    defaults.update(params)
    return PlanetariumDome.objects.create(**defaults)


def sample_show(**params):
    defaults = {
        "title": "Test Show",
        "description": "A test show description.",
    }
    defaults.update(params)
    return AstronomyShow.objects.create(**defaults)


def sample_session(show, dome, **params):
    defaults = {
        "show_time": timezone.now(),
    }
    defaults.update(params)
    return ShowSession.objects.create(
        astronomy_show=show, planetarium_dome=dome, **defaults
    )


class UnauthenticatedTicketsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("planetarium:tickets-list")

    def test_auth_required(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedReservationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass123",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)
        self.dome = sample_dome()
        self.show = sample_show()
        self.session = sample_session(self.show, self.dome)
        self.reservation_url = reverse("planetarium:reservations-list")

    def test_create_reservation_with_tickets_successful(self):
        payload = {
            "tickets": [
                {
                    "row": 1,
                    "seat": 1,
                    "show_session": self.session.id,
                }
            ]
        }
        res = self.client.post(self.reservation_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Reservation.objects.count(), 1)
        ticket = Ticket.objects.first()
        self.assertEqual(ticket.row, 1)
        self.assertEqual(ticket.seat, 1)

    def test_create_reservation_with_ticket_invalid_row(self):
        payload = {
            "tickets": [
                {
                    "row": self.dome.rows + 1,
                    "seat": 1,
                    "show_session": self.session.id,
                }
            ]
        }
        res = self.client.post(self.reservation_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid row number", str(res.data))

    def test_create_reservation_with_ticket_invalid_seat(self):
        payload = {
            "tickets": [
                {
                    "row": 1,
                    "seat": self.dome.seats_in_row + 1,
                    "show_session": self.session.id,
                }
            ]
        }
        res = self.client.post(self.reservation_url, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid seat number", str(res.data))

    def test_create_reservation_with_ticket_unique_together_fail(self):
        self.client.post(
            self.reservation_url,
            {
                "tickets": [
                    {
                        "row": 1,
                        "seat": 1,
                        "show_session": self.session.id,
                    }
                ]
            },
            format="json",
        )
        payload_2 = {
            "tickets": [
                {
                    "row": 1,
                    "seat": 1,
                    "show_session": self.session.id,
                }
            ]
        }
        res = self.client.post(self.reservation_url, payload_2, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "The fields row, seat, show_session must make a unique set.", str(res.data)
        )
