from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from planetarium.models import (
    Reservation,
    AstronomyShow,
    ShowSession,
    PlanetariumDome,
    Ticket,
)
from planetarium.serializers import ReservationListSerializer

User = get_user_model()


def sample_dome(**params):
    defaults = {
        "name": "Main Dome",
        "rows": 10,
        "seats_in_row": 12,
    }
    defaults.update(params)
    return PlanetariumDome.objects.create(**defaults)


def sample_show(**params):
    defaults = {
        "title": "Stars and Beyond",
        "description": "A journey through space",
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


def sample_ticket(reservation, session, **params):
    defaults = {
        "row": 1,
        "seat": 1,
        "show_session": session,
    }
    defaults.update(params)
    return Ticket.objects.create(reservation=reservation, **defaults)


class PublicReservationTests(APITestCase):
    def test_auth_required(self):
        url = reverse("planetarium:reservations-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedReservationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="testpass123",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

        self.dome = sample_dome()
        self.show = sample_show()
        self.session = sample_session(self.show, self.dome)

    def test_list_reservations(self):
        reservation = Reservation.objects.create(user=self.user)
        sample_ticket(reservation=reservation, session=self.session)

        url = reverse("planetarium:reservations-list")
        res = self.client.get(url)

        reservations = Reservation.objects.filter(user=self.user)
        serializer = ReservationListSerializer(reservations, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_create_reservation_with_ticket(self):
        payload = {
            "tickets": [
                {
                    "row": 3,
                    "seat": 5,
                    "show_session": self.session.id,
                }
            ]
        }

        url = reverse("planetarium:reservations-list")
        res = self.client.post(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 1)
        ticket = Ticket.objects.first()
        self.assertEqual(ticket.row, 3)
        self.assertEqual(ticket.seat, 5)
        self.assertEqual(ticket.show_session, self.session)

    def test_update_reservation_not_allowed(self):
        reservation = Reservation.objects.create(user=self.user)
        url = reverse("planetarium:reservations-detail", args=[reservation.id])
        res = self.client.put(url, {})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_reservation(self):
        reservation = Reservation.objects.create(user=self.user)
        url = reverse("planetarium:reservations-detail", args=[reservation.id])

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reservation.objects.filter(id=reservation.id).exists())
