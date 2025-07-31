from django.contrib import admin

from .models import PlanetariumDome, Reservation, AstronomyShow, ShowSession, Ticket, ShowTheme


admin.site.register(PlanetariumDome)
admin.site.register(Reservation)
admin.site.register(AstronomyShow)
admin.site.register(ShowSession)
admin.site.register(Ticket)
admin.site.register(ShowTheme)
