from django.contrib import admin

from .models import (
    PlanetariumDome,
    Reservation,
    AstronomyShow,
    ShowSession,
    Ticket,
    ShowTheme,
)


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


class ReservationAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)


admin.site.register(PlanetariumDome)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(AstronomyShow)
admin.site.register(ShowSession)
admin.site.register(Ticket)
admin.site.register(ShowTheme)
