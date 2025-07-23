from django.db import models


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self) -> str:
        return f"Planetarium: {self.name} (id: {self.id}) (row: {self.rows} seat: {self.seats_in_row})"

