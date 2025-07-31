from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.constraints import UniqueConstraint

from app import settings


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self) -> str:
        return f"Planetarium: {self.name} (id: {self.id}) (row: {self.rows} seat: {self.seats_in_row})"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Reservation: {self.created_at} User: {self.user}"


class AstronomyShow(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    themes = models.ManyToManyField("ShowTheme", related_name="shows")

    def __str__(self):
        return f"Astronomy Show: {self.title} Description: {self.description}"


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE)
    planetarium_dome = models.ForeignKey(PlanetariumDome, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    class Meta:
        indexes = [models.Index(fields=["show_time"])]
        constraints = [
            models.UniqueConstraint(fields=["planetarium_dome", "show_time"], name="unique_dome_session")
        ]

    def __str__(self) -> str:
        return f"Session: {self.show_time}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(ShowSession, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)

    class Meta:
        constraints = [UniqueConstraint(fields=["row", "seat", "show_session"], name="unique_ticket")]

    def __str__(self) -> str:
        return f"Ticket: Row {self.row}, Seat {self.seat}, Session {self.show_session.show_time}"

    def clean(self):
        dome = self.show_session.planetarium_dome

        if not (1 <= self.row <= dome.rows):
            raise ValidationError(f"Invalid row number {self.row}. Max rows: {dome.rows}.")

        if not (1 <= self.seat <= dome.seats_in_row):
            raise ValidationError(f"Invalid seat number {self.seat}. Max seats per row: {dome.seats_in_row}.")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        return super(Ticket, self).save(force_insert, force_update, using, update_fields)


class ShowTheme(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"ShowTheme: {self.name}"
