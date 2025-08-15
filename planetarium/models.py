import pathlib
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from app import settings


def planetarium_dome_image_path(
    instance: "PlanetariumDome", filename: str
) -> pathlib.Path:
    filename = (
        f"{slugify(instance.name)}-{uuid.uuid4()}" + pathlib.Path(filename).suffix
    )
    return pathlib.Path("upload/planetarium_dome") / pathlib.Path(filename)


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    image = models.ImageField(
        upload_to=planetarium_dome_image_path, null=True, blank=True
    )

    @property
    def total_seats(self) -> int:
        return self.rows * self.seats_in_row

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
            models.UniqueConstraint(
                fields=["planetarium_dome", "show_time"], name="unique_dome_session"
            )
        ]

    def __str__(self) -> str:
        return f"Session: {self.show_time}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(
        ShowSession, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        unique_together = ("row", "seat", "show_session")
        ordering = ["row", "seat", "show_session"]

    def __str__(self) -> str:
        return f"Ticket: Row {self.row}, Seat {self.seat}, Session {self.show_session.show_time}"

    def clean(self):
        dome = self.show_session.planetarium_dome

        if not (1 <= self.row <= dome.rows):
            raise ValidationError(
                f"Invalid row number {self.row}. Max rows: {dome.rows}."
            )

        if not (1 <= self.seat <= dome.seats_in_row):
            raise ValidationError(
                f"Invalid seat number {self.seat}. Max seats per row: {dome.seats_in_row}."
            )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )


class ShowTheme(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return f"ShowTheme: {self.name}"
